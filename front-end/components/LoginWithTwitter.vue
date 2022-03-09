<template>
    <b-jumbotron header="Login with Twitter">
        <p>Only whitelisted users can use this app</p>
        <b-button variant="primary" @click="loginWithTwitter()">Login</b-button>
    </b-jumbotron>
</template>

<script>
export default {
    name: 'LoginWithTwitter',
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