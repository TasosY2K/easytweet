<template>
  <div class="container">
      <div v-if="authenticated == null" class="spinner-cls">
        <b-spinner class="spinner-border text-light"></b-spinner>
      </div>
      <div v-else class="center">
        <div class="row">
          <div class="col-md-6 offset-md-3">
            <LoginWithTwitter v-if="authenticated == false" />
            <div v-else-if="authenticated" >
              <div class="mb-2">
                <b-button @click="componentViewHandler('collector')" variant="primary" class="nav-button">Data collection</b-button>
                <b-button @click="componentViewHandler('monitor')" variant="primary" class="nav-button">Monitor</b-button>
                <b-button @click="componentViewHandler('logs')" variant="primary" class="nav-button">Logs</b-button>
                <b-button @click="logout()" class="nav-button" variant="primary">Logout</b-button>
              </div>
              <DataCollector v-if="componentView == 'collector'"/>
              <Monitor v-else-if="componentView == 'monitor'"/>
              <Logs v-else-if="componentView == 'logs'" />
            </div>
          </div>
        </div>
      </div>        
    <div class="footer">© Datalab, Aristotle Uni. of Thessaloniki</div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Lato&display=swap');

.btn:focus,.btn:active {
   outline: none !important;
   box-shadow: none;
}

textarea:focus, 
textarea.form-control:focus, 
input.form-control:focus, 
input[type=text]:focus, 
input[type=password]:focus, 
input[type=email]:focus, 
input[type=number]:focus, 
[type=text].form-control:focus, 
[type=password].form-control:focus, 
[type=email].form-control:focus, 
[type=tel].form-control:focus, 
[contenteditable].form-control:focus {
  box-shadow: inset 0 -1px 0 #ddd;
}

body {
  font-family: 'Lato', sans-serif;
  background-color: #000000;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 100 100'%3E%3Crect x='0' y='0' width='3' height='3' fill-opacity='0.6' fill='%23FFFFFF'/%3E%3C/svg%3E");
}

.center {
  min-width: 80%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.spinner-cls {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.jumbo {
  background-color: #fff !important;
  padding: 2rem;
  border-radius: 10px;
}

.border-radius {
  border-radius: 10px !important;
}

.footer {
  color: #fff;
  position: absolute;
  left: 41%;
  bottom: 0;
  height: 60px;
  line-height: 60px;
}

.nav-button {
  border-radius: 10px;
}

.nav-button:active {
  transform: translateY(4px);
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
      componentView: "collector",
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
