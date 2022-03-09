<template>
  <div v-if="authenticated == null" class="center">
    <b-spinner></b-spinner>
  </div>
  <div v-else class="container center">
    <div class="row">
        <div class="col-md-6 offset-md-3">
          <LoginWithTwitter v-if="authenticated == false" />
          <div v-else-if="authenticated" >
            <b-button-group>
              <b-button @click="componentViewHandler('collector')">Data collection</b-button>
              <b-button @click="componentViewHandler('monitor')">Monitor</b-button>
              <b-button @click="componentViewHandler('logs')">Logs</b-button>
              <b-button @click="logout()">Logout</b-button>
            </b-button-group>
            <DataCollector v-if="componentView == 'collector'"/>
            <Monitor v-else-if="componentView == 'monitor'"/>
            <Logs v-else-if="componentView == 'logs'" />
          </div>
        </div>
    </div>
  </div>
</template>

<style scoped>
.center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>

<script>
import LoginWithTwitter from "../components/LoginWithTwitter.vue";
import DataCollector from '../components/DataCollector.vue';
import Monitor from '../components/Monitor.vue';
export default {
  components: { LoginWithTwitter, DataCollector, Monitor },
  name: 'IndexPage',
  methods: {
    logout() {
      localStorage.removeItem("userInfo");
      window.location.href = "/";
    },
    componentViewHandler(view) {
        this.componentView = view;
    }
  },
  data() {
    return {
      authenticated: null,
      componentView: "collector"
    }
  },
  mounted() {
    const userInfo = localStorage.getItem("userInfo");
    if (userInfo && userInfo.length > 0 && Object.keys(userInfo).length !== 0) {
      this.authenticated = true;
    } else {
      this.authenticated = false;
    }
  }
}
</script>
