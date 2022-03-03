<template>
  <LoginWithTwitter v-if="!authenticated" />
  <DataCollector v-else />
</template>

<script>
import LoginWithTwitter from "../components/LoginWithTwitter.vue";
import DataCollector from '../components/DataCollector.vue';
export default {
  components: { LoginWithTwitter, DataCollector },
  name: 'IndexPage',
  data() {
    return {
      authenticated: false
    }
  },
  mounted() {
    const userInfo = localStorage.getItem("userInfo");
    if (userInfo && userInfo.length > 0 && Object.keys(userInfo).length !== 0) {
      this.authenticated = true;
    } else {
      this.authenticated = false;
    }
    console.log(this.authenticated);
  }
}
</script>
