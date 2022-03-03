<template>
    <b-jumbotron header="Login with Twitter" class="center">
        <p>Only whitelisted users can use this app</p>
        <b-button variant="primary" @click="loginWithTwitter()">Login</b-button>
    </b-jumbotron>
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
export default {
    name: 'IndexPage',
    methods: {
        async loginWithTwitter() {
            const res = await this.$axios.get(`${process.env.apiUrl}/req4req`);
            const oauthToken = res.data.oauth_token;
            const oauthTokenSecret = res.data.oauth_token_secret;
            localStorage.setItem("oauthTokenSecret", oauthTokenSecret);
            window.location.href = `https://api.twitter.com/oauth/authorize?oauth_token=${oauthToken}`;
        }
    }
}
</script>