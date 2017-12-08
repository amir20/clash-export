<template>
  <div>
    <nav class="navbar">
        <div class="navbar-brand">
            <h1 class="navbar-item">
                <img :src="this.meta.badgeUrls.small" alt="Image">
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
                        <div class="control">
                            <a class="button" :class="{'is-warning': days == 30}" @click="loadDaysAgo(30)">
                                Last Month
                            </a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="field is-grouped">
                        <p class="control">
                            <div class="dropdown is-hoverable is-right">
                                <div class="dropdown-trigger">
                                    <button class="button is-danger" aria-haspopup="true" aria-controls="dropdown-menu">
                                      <span class="icon">
                                          <i class="fa fa-download"></i>
                                        </span>
                                        <span>Download</span>
                                        <span class="icon is-small">
                                            <i class="fa fa-angle-down" aria-hidden="true"></i>
                                        </span>
                                    </button>
                                </div>
                                <div class="dropdown-menu" id="dropdown-menu" role="menu">
                                    <div class="dropdown-content">
                                      <a class="dropdown-item" :href="`${this.path}.xlsx`">                                        
                                        Today
                                      </a> 
                                      <hr class="dropdown-divider"> 
                                      <a class="dropdown-item" :href="`${this.path}.xlsx?daysAgo=1`">                                        
                                        Yesterday
                                      </a>  
                                      <a class="dropdown-item" :href="`${this.path}.xlsx?daysAgo=2`">                                        
                                        Two Days Ago
                                      </a>  
                                      <a class="dropdown-item" :href="`${this.path}.xlsx?daysAgo=3`">                                        
                                        Three Days Ago
                                      </a>
                                      <hr class="dropdown-divider">    
                                      <a class="dropdown-item" :href="`${this.path}.xlsx?daysAgo=7`">                                        
                                        Last Week
                                      </a>                                  
                                    </div>
                                </div>
                            </div>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    <section>
      <div v-if="loading" class="has-text-centered load-text">
        <i class="fa fa-spinner fa-2 fa-spin"></i>
      </div>
      <table class="table is-narrow is-fullwidth is-striped" v-if="!loading">
        <thead>
          <tr>
            <th v-for="(header, index) in header" :class="{'selected-sort': index - 2 == sortIndex, 'up': sortDirection == 1, 'down': sortDirection == -1}">
              <a @click="updateSort(index - 2)">{{ header }}</a>
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
            <td>{{ row.tag }}</td>
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
      days: 7,
      sortIndex: 5,
      sortDirection: 1,
      meta: {
        badgeUrls: {
          small: "https://placeholdit.co//i/500x500?text=&bg=ccc"
        }
      }
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
        const [name, tags, ...columns] = row;
        previousPlayers[name] = columns;
      });

      const tableData = clanRows.map(row => {
        const [name, tag, ...columns] = row;
        const previousColumns = previousPlayers[name] || columns;

        const zippedRow = zip(columns, previousColumns);
        const data = zippedRow.map(item => {
          const [now, previous] = item;

          return { now, delta: now - previous, previous };
        });

        return { name, tag, data };
      });


      return tableData.sort((a, b) => {
        if (this.sortIndex == -2) { // index for name
          return a.name.toLowerCase() < b.name.toLowerCase() ? -this.sortDirection : this.sortDirection;
        } else if (this.sortIndex == -1) { // index for name
          return a.tag.toLowerCase() < b.tag.toLowerCase() ? -this.sortDirection : this.sortDirection;
        } else { // index for other columns
          return a.data[this.sortIndex].now < b.data[this.sortIndex].now ? this.sortDirection : -this.sortDirection;
        }
      });
    },
    header() {
      return this.clan[0];
    },
    path() {
      return `/clan/${this.tag.replace('#', '')}`
    }
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const nowPromise = fetch(`${this.path}.json`);
      const previousPromise = fetch(`${this.path}.json?daysAgo=${this.days}`);
      const metaPromise = fetch(`${this.path}/short.json`);
      
      this.meta = await (await metaPromise).json();
      this.previousData = await (await previousPromise).json();
      this.clan = await (await nowPromise).json();          

      this.loading = false;
    },
    async loadDaysAgo(days) {
      this.days = days;
      const data = await fetch(`${this.path}.json?daysAgo=${days}`);
      this.previousData = await data.json();
    },
    updateSort(column) {
      if (this.sortIndex != column) {
        this.sortIndex = column;
      } else {
        this.sortDirection = -this.sortDirection;
      }
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

    &.selected-sort {
      &.up {
        border-top: 4px solid #ff3860;
      }

      &.down {
        border-bottom: 4px solid #ff3860;
      }
    }
  }

  & tr:hover {
    background-color: #00d1b2;
  }

  & a {
    color: #fff;

    &:hover {
      text-decoration: underline;
    }
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

nav {
  box-shadow: 0 2px 3px rgba(10, 10, 10, 0.1);
  position: sticky;
  top: 0;
}

.load-text {
  font-size: 120%;
  margin: 3em 0;
}
</style>

<style>
body {
  overflow-x: initial;
}
</style>