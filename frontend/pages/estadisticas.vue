<template>
  <div>
    <portal to="header">
      <div class="hero-body">
        <h1 class="title">
          Estadísticas Generales
        </h1>
      </div>
    </portal>

    <stats-top-relation />
    <stats-cases-by-year />
    <stats-judges />
    <satats-oral />
    <stats-crimes />
    <stats-old-cases />
    <stats-duration />
  </div>
</template>

<script>
import StatsTopRelation from '@/components/StatsTopRelation'
import StatsCasesByYear from '@/components/StatsCasesByYear'
import StatsJudges from '@/components/StatsJudges'
import SatatsOral from '@/components/SatatsOral'
import StatsCrimes from '@/components/StatsCrimes'
import StatsOldCases from '@/components/StatsOldCases'
import StatsDuration from '@/components/StatsDuration'

export default {
  head () {
    return {
      title: 'Estadisticas Generales'
    }
  },
  components: {
    StatsTopRelation,
    StatsCasesByYear,
    StatsJudges,
    SatatsOral,
    StatsCrimes,
    StatsOldCases,
    StatsDuration
  }
}
</script>
