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
       <b-table
            :data="tableData"            
            striped
            narrowed
            hoverable
            mobile-cards
            default-sort="currentTrophies"
            default-sort-direction="desc"            
            :loading="loading">
             <template slot-scope="props">
                <b-table-column v-for="column in header" :label="column.label" :field="`${column.field}.value`" :key="column.field" :numeric="column.numeric" sortable>
                    {{ props.row[column.field].value.toLocaleString() }}
                </b-table-column>
            </template>            
        </b-table>    
    </section>
  </div>
</template>

<script>
import zip from "lodash/zip";
import camelCase from "lodash/camelCase";
import reduce from "lodash/reduce";
import keyBy from "lodash/keyBy";
import isNumber from "lodash/isNumber";
import fakeData from "../fake-data";

export default {
  props: ["tag", "name"],
  data() {
    return {
      loading: true,
      clan: fakeData,
      previousData: fakeData,
      days: 7,
      meta: {
        badgeUrls: {
          small: "https://placeholdit.co//i/500x500?text=&bg=ccc"
        }
      }
    };
  },
  created() {
    this.fetchData();
  },
  computed: {
    tableData() {
      const data = this.convertToMap(this.clan.slice(1));
      const previousData = this.convertToMap(this.previousData.slice(1));
      const previousByTag = keyBy(previousData, "tag");

      return data.map(row => {
        const previousRow = previousByTag[row.tag];
        return reduce(
          row,
          (map, value, column) => {
            const delta =
              previousRow && isNumber(value)
                ? previousRow[column] - value
                : 0;

            map[column] = { value, delta };
            return map;
          },
          {}
        );
      });
    },
    header() {
      return this.clan[0].map((column, index) => ({
        label: column,
        field: camelCase(column),
        numeric: index > 1
      }));
    },
    path() {
      return `/clan/${this.tag.replace("#", "")}`;
    }
  },
  methods: {
    async fetchData() {
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
    convertToMap(matrix) {
      const header = this.header;
      return matrix.map(row => {
        return reduce(
          row,
          (map, value, columnIndex) => {
            map[header[columnIndex].field] = value;
            return map;
          },
          {}
        );
      });
    }
  }
};
</script>

<style scoped>
.b-table {
  &>>>table {
    font-size: 90%;
  }

  &>>>thead {
    background-color: #00d1b2;

    & th {
      color: #fff;
    }
  }

  &.is-loading * {
    color: #efefef !important;
  }
}

section {
  overflow-y: scroll;
}

h1 {
  font-size: 140%;
}

nav {
  box-shadow: 0 2px 3px rgba(10, 10, 10, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}
</style>

<style>
body {
  overflow-x: initial;
}
</style>