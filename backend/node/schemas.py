from marshmallow import Schema, fields, validate


class Query(Schema):
    show = fields.Str(
      default='full',
      validate=validate.OneOf(['full', 'short']),
      description='Mostrar todo la info del nodo o solo un resumen',
    )


class Relations(Schema):
    denunciante = fields.Int()
    querellante = fields.Int()
    sobreseido = fields.Int()
    investigado = fields.Int()


class Metrics(Schema):
    outdegree = fields.Int()
    indegree = fields.Int()
    degree = fields.Int()


class Radications(Schema):
    camara = fields.Str()
    fecha = fields.Str()
    fiscal = fields.Str()
    fiscalia = fields.Str()
    juez_1 = fields.Str()
    juez_2 = fields.Str()
    juez_3 = fields.Str()
    organo_nombre = fields.Str()
    organo_tipo = fields.Str()
    sala = fields.Str()
    _fiscal = fields.Str()


class Resolution(Schema):
    camara = fields.Str()
    fecha = fields.Str()
    pdf_hash = fields.Str()
    pdf_nombre = fields.Str()
    pdf_url = fields.Str()
    resuelve_texto = fields.Str()
    sala = fields.Str()


class Involve(Schema):
    key = fields.Str()
    nombre = fields.Str()
    relacion = fields.Str()


class Cases(Schema):
    _id = fields.Str()
    _key = fields.Str()
    _rev = fields.Str()
    anio_comienzo = fields.Int()
    caratula = fields.Str()
    estado = fields.Str()
    expediente = fields.Str()
    fecha_inicio = fields.Str()
    fiscal = fields.Str()
    fuente_foto = fields.Str()
    hechos = fields.Str()
    juez = fields.Str()
    nombre = fields.Str()
    notas = fields.Str()
    tipo = fields.Str()
    ultima_actualizacion = fields.Str()
    terminado = fields.Bool()
    delitos = fields.List(fields.Str())
    radicaciones = fields.List(fields.Nested(Radications))
    resoluciones = fields.List(fields.Nested(Resolution))
    involucrados = fields.List(fields.Nested(Involve))
    metricas = fields.Nested(Metrics)


class CasesNode(Schema):
    execution_time = fields.Float()
    causa = fields.Nested(Cases)


class Entity(Schema):
    _id = fields.Str()
    _key = fields.Str()
    _rev = fields.Str()
    nombre = fields.Str()
    tipo = fields.Str()
    sub_tipo = fields.Str()
    foto = fields.Str()
    bio = fields.Str()
    cardinal = fields.Int()
    causas = fields.List(fields.Dict())
    relaciones = fields.Nested(Relations)
    metricas = fields.Nested(Metrics)


class EntityNode(Schema):
    execution_time = fields.Float()
    entidad = fields.Nested(Entity)


class Magistrate(Schema):
    _id = fields.Str()
    _key = fields.Str()
    _rev = fields.Str()
    camara = fields.Str()
    cargo_cobertura = fields.Str()
    cargo_fecha_jura = fields.Str()
    cargo_licencia = fields.Str()
    cargo_tipo = fields.Str()
    cargo_vacante = fields.Str()
    concurso_ambito = fields.Str()
    concurso_ambito_fecha_ingreso = fields.Str()
    concurso_en_tramite = fields.Str()
    concurso_numero = fields.Str()
    justicia_federal_o_nacional = fields.Str()
    magistrado_dni = fields.Int()
    magistrado_genero = fields.Str()
    nombre = fields.Str()
    norma_fecha = fields.Str()
    norma_ministro = fields.Str()
    norma_numero = fields.Str()
    norma_presidente = fields.Str()
    norma_tipo = fields.Str()
    orden = fields.Int()
    organo_habilitado = fields.Str()
    organo_nombre = fields.Str()
    organo_provincia = fields.Str()
    organo_provincia_id = fields.Int()
    organo_tipo = fields.Str()
    presidente_camara = fields.Str()
    subrogancia_fecha_vencimiento = fields.Str()
    subrogante_calidad = fields.Str()
    subtipo = fields.Str()
    tipo = fields.Str()
    titular_con_licencia = fields.Str()
    titular_con_licencia_dni = fields.Str()
    titular_con_licencia_genero = fields.Str()
    casos_importantes = fields.List(fields.Dict())
    mas_investigados = fields.List(fields.Dict())
    histo_causas_abiertas = fields.List(fields.Dict())
    histo_causas_cerradas = fields.List(fields.Dict())
    metricas = fields.Nested(Metrics)


class MagistrateNode(Schema):
    execution_time = fields.Float()
    magistrado = fields.Nested(Magistrate)
