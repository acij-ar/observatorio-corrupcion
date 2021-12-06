<template>
  <div>
    <portal to="header">
      <div class="hero-body">
        <h1 class="title">
          Quiénes somos
        </h1>
      </div>
    </portal>

    <section class="container has-text-centered description py-6">
      <p>
        El Observatorio de Causas de Corrupción es una iniciativa de la Asociación
        Civil por la Igualdad y la Justicia (ACIJ), desarrollada en conjunto
        con la Fundación Conocimiento Abierto.
      </p>
      <p>
        La <a href="https://acij.org.ar/" target="_blank">Asociación Civil por la Igualdad y la Justicia (ACIJ)</a> es una organización
        apartidaria, sin fines de lucro, dedicada a la defensa de los derechos de los
        grupos más desfavorecidos de la sociedad y el fortalecimiento de la democracia en Argentina.
        <br>
        Fundada en 2002, ACIJ tiene por objetivos defender la efectiva vigencia de la Constitución
        Nacional y los principios del estado de derecho, promover el cumplimiento de las leyes
        que protegen a los grupos desaventajados y la erradicación de toda práctica discriminatoria,
        así como también contribuir al desarrollo de prácticas participativas y deliberativas de la democracia.
      </p>
      <p>
        <a href="https://conocimientoabiert.org/" target="_blank">Conocimiento Abierto</a> es una organización que tiene la misión de fortalecer la democracia
        digital para potenciar la calidad de la participación ciudadana, el acceso a la información
        y los derechos digitales en América Latina.
      </p>
    </section>
  </div>
</template>

<script>
export default {
  head () {
    return {
      title: 'Nosotros'
    }
  },
}
</script>
