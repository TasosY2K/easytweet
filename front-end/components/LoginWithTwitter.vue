<template>
    <b-jumbotron class="jumbo" header="Login">
        <p>You must have the secret token to use this application</p>
        <span>Secret token:</span>
        <b-input class="border-radius" type="text" v-model="secretToken" @input="checkToken()" ></b-input>
        <span v-if="secretTokenValidated" class="text-success">Token validated</span>
        <span v-else class="text-danger">Token not validated</span>
        <hr/>
        <b-button :disabled="buttonDisabled" class="border-radius" variant="primary" @click="loginWithTwitter()">Login</b-button>
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
        },
        async checkToken() {
            this.$axios.setHeader("Authorization", this.secretToken)
            
            try {
                const res = await this.$axios.get(`${process.env.apiUrl}/`);

                if (res.status == 200) {
                    this.secretTokenValidated = true
                    this.buttonDisabled = false
                } else {
                    this.secretTokenValidated = false
                    this.buttonDisabled = true
                }

            } catch (error) {
                this.secretTokenValidated = false
                this.buttonDisabled = true
            }
        }
    },
    data() {
        return {
            secretToken: null,
            secretTokenValidated: false,
            buttonDisabled: true
        }
    }
}
</script>