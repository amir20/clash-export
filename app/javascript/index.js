import Vue from 'vue'
import Clan from './Clan'

if (document.getElementById('clan-table')) {
  new Vue({
    el: '#clan-table',
    components: {
      Clan
    }
  });
}