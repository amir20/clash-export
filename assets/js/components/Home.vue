<template>
  <form class="section" action="/search" method="get" @reset="onReset">
    <template v-if="savedTag">
      <section class="hero">
        <div class="hero-body">
          <h1 class="title is-1">Hey there, {{ hasUser ? userName : "chief" }}!</h1>
          <h2 class="subtitle">I found your clan! Let's continue or start over again.</h2>
        </div>
      </section>
      <card :tag="savedTag" @error="onClanError" :found-clan.sync="fetchedClan"></card>
      <b-modal :active.sync="showModal" has-modal-card v-if="!skipPlayerQuestion && fetchedClan && !hasUser">
        <div class="modal-card">
          <header class="modal-card-head"></header>
          <section class="modal-card-body">
            <div class="columns">
              <div class="column">
                <h3 class="subtitle is-3">Chief, tell me who you are!</h3>
                I found <b>{{ fetchedClan.players.length }}</b> players in <b>{{ fetchedClan.name }}</b
                >. If you are one of these players, then I can remember next time. I will make suggestions or compare you against other players. This optional
                so if you don't me to remember just skip it. You can always manage your profile later.
              </div>
              <div class="column is-narrow is-hidden-mobile"><web-p-image name="builder-show" width="200" /></div>
            </div>
            <player-list :players="fetchedClan.players" @update:selectedPlayer="onPlayerSelected"></player-list>
          </section>
          <footer class="modal-card-foot">
            <button class="button is-warning" type="button" @click="onSkip">Skip this step</button>
          </footer>
        </div>
      </b-modal>
      <p class="buttons">
        <button type="reset" class="button is-warning is-large">Reset</button>
        <a :href="`/clan/${foundClan ? foundClan.slug : ''}`" class="button is-success is-large" :disabled="foundClan == null">{{
          foundClan ? foundClan.name : "Your Clan"
        }}</a>
        <a :href="`/player/${userSlug}`" class="button is-info is-large" v-if="hasUser" :disabled="userSlug == null">
          <b-icon pack="fas" icon="user"></b-icon>
          <span>Your Profile</span>
        </a>
      </p>
    </template>
    <template v-else>
      <section class="hero">
        <div class="hero-body">
          <h1 class="title is-1">Hey, Chief!</h1>
          <h2 class="subtitle">
            Welcome to Clash Leaders. This website shows trending clans in Clash of Clans game. Clan achievements can be exported to a spreadsheet or compared
            to historical data over time. Let's start by finding your clan first.
          </h2>
        </div>
      </section>
      <div class="column field">
        <p class="control"><search-box @update:selectedTag="setSavedClan" size="is-large"></search-box></p>
      </div>
    </template>
  </form>
</template>

<script>
import Card from "./ClanCard";
import SearchBox from "./SearchBox";
import PlayerList from "./PlayerList";
import WebPImage from "./WebPImage";
import UserMixin from "../user";
import { mapMutations, mapState } from "vuex";

export default {
  components: {
    Card,
    SearchBox,
    PlayerList,
    WebPImage,
  },
  mixins: [UserMixin],
  data() {
    return {
      fetchedClan: null,
      showModal: true,
    };
  },
  methods: {
    ...mapMutations(["setSavedClan", "clearSavedTag", "doNotAskForPlayer", "setSavedPlayer"]),
    onReset() {
      this.showModal = true;
      this.clearSavedTag();
    },
    onSkip() {
      this.doNotAskForPlayer();
      this.showModal = false;
    },
    onClanError() {
      this.clearSavedTag();
    },
    onPlayerSelected(player) {
      this.setSavedPlayer(player);
      this.showModal = false;
    },
    prefetch(url) {
      const link = document.createElement("link");
      link.href = url;
      link.rel = "prefetch";
      link.as = "fetch";
      document.head.appendChild(link);
    },
  },
  watch: {
    foundClan(newValue) {
      if (newValue) {
        this.prefetch(`/clan/${newValue.slug}`);
      }
    },
  },
  computed: {
    ...mapState(["foundClan", "savedTag", "savedPlayer", "skipPlayerQuestion"]),
  },
};
</script>
<style lang="scss" scoped>
a[disabled="disabled"] {
  pointer-events: none;
}

.modal-card {
  max-width: 900px;
  width: 100%;
  max-height: calc(95vh);
}
</style>
