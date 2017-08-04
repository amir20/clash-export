<template>
  <div>
    <nav class="navbar has-shadow">
      <div class="navbar-brand">
        <h1 class="navbar-item">
          {{ name }}
        </h1>
      </div>
      <div class="navbar-menu">
        <div class="navbar-start">
          <div class="navbar-item">
            <div class="field has-addons">
              <div class="control">
                <a class="button" :class="{'is-warning': days == 1}" @click="loadDaysAgo(1)">
                  Yesterday
                </a>
              </div>
              <div class="control">
                <a class="button" :class="{'is-warning': days == 7}" @click="loadDaysAgo(7)">
                  Last Week
                </a>
              </div>              
            </div>
          </div>
        </div>
        <div class="navbar-end">
          <div class="navbar-item">
            <div class="field is-grouped">
              <p class="control">
                <a class="button is-danger" :href="`/clan/${encodeURIComponent(tag)}.xlsx`">
                  <span class="icon">
                    <i class="fa fa-download"></i>
                  </span>
                  <span>Export</span>
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <section>
      <div class="has-text-centered" v-if="loading">Please wait...</div>
      <table class="table is-narrow is-fullwidth is-striped" v-if="!loading">
        <thead>
          <tr>
            <th v-for="header in header">
              {{ header }}
            </th>
          </tr>
        </thead>
        <tfoot>
          <tr>
            <th v-for="header in header">
              {{ header }}
            </th>
          </tr>
        </tfoot>
        <tbody>
          <tr v-for="row in tableData">
            <th>{{ row.name }}</th>
            <td v-for="column in row.data">
              {{ column.now.toLocaleString() }}
              <b v-if="column.delta != 0" :class="{up: column.delta > 0, down: column.delta < 0}">
                <i :class="{'fa-arrow-up': column.delta > 0, 'fa-arrow-down': column.delta < 0, fa: true}" aria-hidden="true"></i> {{ Math.abs(column.delta).toLocaleString() }}</b>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  
  </div>
</template>

<script>
import zip from 'lodash/zip'

export default {
  props: ['tag', 'name'],
  data() {
    return {
      loading: false,
      clan: null,
      previousData: null,
      days: 7
    }
  },
  created() {
    this.fetchData();
  },
  computed: {
    tableData() {
      const clanRows = this.clan.slice(1);

      // Map by user -> columns      
      const previousPlayers = {};
      this.previousData.slice(1).forEach(row => {
        const [name, ...columns] = row;
        previousPlayers[name] = columns;
      });

      return clanRows.map(row => {
        const [name, ...columns] = row;
        const previousColumns = previousPlayers[name] || columns;

        const zippedRow = zip(columns, previousColumns);
        const data = zippedRow.map(item => {
          const [now, previous] = item;

          return { now, delta: now - previous, previous };
        });

        return { name, data };
      });
    },
    header() {
      return this.clan[0];
    }
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const nowPromise = fetch(`/clan/${encodeURIComponent(this.tag)}.json`);
      const previousPromise = fetch(`/clan/${encodeURIComponent(this.tag)}.json?daysAgo=${this.days}`);

      const nowResponse = await nowPromise;
      const previousResponse = await previousPromise;

      this.clan = await nowResponse.json();
      this.previousData = await previousResponse.json();

      this.loading = false;
    },
    async loadDaysAgo(days) {
      this.days = days;
      const data = await fetch(`/clan/${encodeURIComponent(this.tag)}.json?daysAgo=${days}`);
      this.previousData = await data.json();
    }
  }
}
</script>

<style scoped>
table {
  font-size: 90%;
}

thead {
  background-color: #00d1b2;

  & th {
    color: #fff;
  }

  & tr:hover {
    background-color: #00d1b2;
  }
}

section {
  overflow-y: scroll;
  max-width:
}

h1 {
  font-size: 140%;
}

b {
  white-space: nowrap;
  display: block;
  line-height: 1;
  margin-top: 5px;
  font-size: 95%;

  &.up {
    color: #23d160;
  }

  &.down {
    color: #ff3860;
  }
}
</style>
