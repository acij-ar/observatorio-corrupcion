import collections

import numpy as np
from flask_restful import Resource, abort
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

from plugins import cache
from session import arangoDB
from node import schemas


class CasesNode(MethodResource, Resource):
    @doc(description='Obtener una causa', tags=['Nodos'])
    @use_kwargs(schemas.Query, location="query")
    @marshal_with(schemas.CasesNode)
    @cache.cached(query_string=True)
    def get(self, document: str, show: str = 'full'):
        document = ' '.join(document.split())
        if not document:
            text = "El nombre del nodo tiene que ser especificado"
            abort(404, message=text)

        document = document.replace(' ', '_').replace('-', '_')
        parameters = {'node': f'nodos_causas/{document}'}

        return query_cases(parameters, show)


class EntityNode(MethodResource, Resource):
    @doc(description='Obtener una entidad', tags=['Nodos'])
    @use_kwargs(schemas.Query, location="query")
    @marshal_with(schemas.EntityNode)
    @cache.cached(query_string=True)
    def get(self, document: str, show: str = 'full'):
        document = ' '.join(document.split())
        if not document:
            text = "El nombre del nodo tiene que ser especificado"
            abort(404, message=text)

        document = document.replace(' ', '_').replace('-', '_')
        parameters = {'node': f'nodos_entidades/{document}'}

        return query_entity(parameters, show)


class MagistrateNode(MethodResource, Resource):
    @doc(description='Obtener un magistrado', tags=['Nodos'])
    @use_kwargs(schemas.Query, location="query")
    @marshal_with(schemas.MagistrateNode)
    @cache.cached(query_string=True)
    def get(self, document: str, show: str = 'full'):
        document = ' '.join(document.split())
        if not document:
            text = "El nombre del nodo tiene que ser especificado"
            abort(404, message=text)

        document = document.replace(' ', '_').replace('-', '_')
        parameters = {'node': f'nodos_magistrados/{document}'}

        return query_magistrate(parameters, show)


def query_entity(parameters, show):
    """

    """
    query_full = """
    LET cases = (
        FOR v, e IN 1..1 OUTBOUND @node GRAPH 'grafo'
            FILTER v.tipo == 'expediente judicial'

            LET involucrados = (
                FOR v2, e2 IN 1..1 ANY v._id GRAPH 'grafo'
                    RETURN {nombre: v2.nombre, key: v2._key, organo_nombre: v2.organo_nombre, relacion: e2.tipo}
            )

            RETURN {
                _key: v._key,
                anio_comienzo: v.anio_comienzo,
                expediente: v.expediente,
                nombre: v.nombre,
                delitos: v.delitos,
                estado: v.estado,
                ultima_actualizacion: v.ultima_actualizacion,
                relacion: e.tipo,
                involucrados: involucrados
            }
    )

    LET d = DOCUMENT(@node)
    RETURN MERGE(d, {causas: cases})
    """

    query_sort = "RETURN DOCUMENT(@node)"

    bind_vars = {
        'node': parameters['node']
    }

    if show == 'full':
        query = query_full
    else:
        query = query_sort

    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    entidad = [r for r in data][0] or {}

    if show == 'full' and entidad['tipo'] == 'organismo estatal':
        query = """
        FOR v, e IN 1..1 ANY @node GRAPH 'grafo'
            FILTER e.tipo == 'querellante'

            FOR v2, e2 IN 1..1 ANY v._id GRAPH 'grafo'
                FILTER e2.tipo == 'investigado'
                RETURN v2.nombre
        """
        entities = arangoDB.aql.execute(query, bind_vars=bind_vars)
        entities = [r for r in entities]

        counter = collections.Counter(entities)
        commons = [
            {'name': i[0], 'value': i[1]}
            for i in counter.most_common(10)
        ]
        entidad['querellantes'] = commons

    if 'causas' in entidad:
        for i, cases in enumerate(entidad['causas']):
            judge = [j for j in cases['involucrados'] if j['relacion'] == 'juez']
            if judge and judge[0]['nombre'] != None:
                s = judge[0]['organo_nombre'].split()
                entidad['causas'][i]['juez'] = {
                    "nombre": f"Juzgado Nº {s[-1]} ({judge[0]['nombre']})",
                    "key": judge[0]["key"],
                }
            else:
                entidad['causas'][i]['juez'] = {'nombre': '', '_key': ''}
            prosecutor = [p for p in cases['involucrados'] if p['relacion'] == 'fiscal']
            if prosecutor and prosecutor[0]['nombre'] != None:
                s = prosecutor[0]['organo_nombre'].split()
                entidad['causas'][i]['fiscal'] = {
                    "nombre": f"Fiscalía Nº {s[2]} ({prosecutor[0]['nombre']})",
                    "key": judge[0]["key"],
                }
            else:
                entidad['causas'][i]['fiscal'] = {'nombre': '', '_key': ''}

            entidad['causas'][i]['involucrados'] = [
                invo
                for invo in cases['involucrados']
                if invo['relacion'] not in ['juez', 'fiscal']
            ]

    if show != 'full':
        entidad = {
            key: entidad[key] for key in entidad.keys()
            if key not in ['causas', 'relaciones']
        }

    return {
        'entidad': entidad,
        'execution_time': data.statistics()['execution_time']
    }


def query_cases(parameters, show):
    """

    """
    query_full = """
    LET involucrados = (
        FOR v, e IN 1..1 ANY @node GRAPH 'grafo'
            RETURN {nombre: v.nombre, key: v._key, relacion: e.tipo}
        )

    RETURN MERGE(DOCUMENT(@node), {involucrados: involucrados})
    """

    query_sort = "RETURN DOCUMENT(@node)"

    if show == 'full':
        query = query_full
    else:
        query = query_sort

    bind_vars = {
        'node': parameters['node']
    }
    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    cases = [r for r in data][0] or {}

    if show != 'full':
        cases = {key: cases[key] for key in cases.keys()
                 if key not in ['delitos', 'resoluciones', 'radicaciones', 'hechos']}

    return {
        'causa': cases,
        'execution_time': data.statistics()['execution_time']
    }


def query_magistrate(parameters, show):
    bind_vars = {
        'node': parameters['node']
    }

    # Get the magistrate data
    query = """
    RETURN DOCUMENT(@node)
    """
    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    magistrate = [r for r in data][0]
    execution_time = data.statistics()['execution_time']

    if show != 'full':
        magistrate = {key: magistrate[key] for key in magistrate.keys()
                      if key in ['_key', 'nombre', 'bio', 'tipo',
                                 'subtipo', 'metricas']}

        return {'magistrado': magistrate,
                'execution_time': execution_time}

    # Get the most commont investigate
    query = """
    FOR v, e IN 1..2 ANY @node GRAPH 'grafo'
        FILTER e.tipo == "investigado"
        // FILTER e.tipo IN ['imputado', 'procesado', 'denunciado']
        RETURN v.nombre
    """
    entities = arangoDB.aql.execute(query, bind_vars=bind_vars)
    entities = [r for r in entities]

    counter = collections.Counter(entities)
    commons = [{'name': i[0], 'value': i[1]} for i in counter.most_common(10)]

    # Get the open cases duration
    query = """
    FOR v, e IN 1..1 ANy @node GRAPH 'grafo'
        FILTER e.tipo == 'juez'
        FILTER v.terminado == false
        RETURN DATE_YEAR(DATE_NOW()) - v.anio_comienzo
    """
    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    years = [r for r in data]

    if years:
        hist, bins = np.histogram(years, bins=[0, 3, 6, 10, 100])
        hist_open = [
            {'bin': '≤ 3 años', 'value': int(hist[0]), 'p': hist[0]*100/len(years)},
            {'bin': '> 3 a 6 años', 'value': int(hist[1]), 'p': hist[1]*100/len(years)},
            {'bin': '> 6 a 10 años', 'value': int(hist[2]), 'p': hist[2]*100/len(years)},
            {'bin': '> 10 años', 'value': int(hist[3]), 'p': hist[3]*100/len(years)}
        ]
    else:
        hist_open = []

    # Get the closed cases duration
    query = """
    FOR v, e IN 1..1 ANy @node GRAPH 'grafo'
        FILTER e.tipo == 'juez'
        FILTER v.terminado == true
        RETURN DATE_YEAR(DATE_NOW()) - v.anio_comienzo
    """
    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    years = [r for r in data]

    if years:
        hist, bins = np.histogram(years, bins=[0, 3, 6, 10, 100])
        hist_close = [
            {'bin': '≤ 3 años', 'value': int(hist[0]), 'p': hist[0]*100/len(years)},
            {'bin': '> 3 a 6 años', 'value': int(hist[1]), 'p': hist[1]*100/len(years)},
            {'bin': '> 6 a 10 años', 'value': int(hist[2]), 'p': hist[2]*100/len(years)},
            {'bin': '> 10 años', 'value': int(hist[3]), 'p': hist[3]*100/len(years)}
        ]
    else:
        hist_close = []

    # Get the importan cases
    query = """
    FOR node, edge IN 1..1 ANY @node GRAPH 'grafo'
        FILTER node.tipo == "expediente judicial"

        LET denunciantes = (FOR node2, edge2 IN 1..1 ANY node GRAPH 'grafo'
            FILTER edge2.tipo == 'denunciante'
            RETURN SPLIT(edge2._from, '/')[1]
        )

        LET querellantes = (FOR node2, edge2 IN 1..1 ANY node GRAPH 'grafo'
            FILTER edge2.tipo == 'querellante'
            RETURN SPLIT(edge2._from, '/')[1]
        )

        RETURN {key:node._key, anio_comienzo: node.anio_comienzo,
                nombre: node.nombre, fiscal: node.fiscal, estado: node.estado,
                ultima_actualizacion: node.ultima_actualizacion,
                denunciantes: denunciantes, querellantes: querellantes}
    """
    data = arangoDB.aql.execute(query, bind_vars=bind_vars)
    cases = [r for r in data]

    #
    magistrate['mas_investigados'] = commons
    magistrate['histo_causas_abiertas'] = hist_open
    magistrate['histo_causas_cerradas'] = hist_close
    magistrate['casos_importantes'] = cases

    return {'magistrado': magistrate,
            'execution_time': execution_time}
