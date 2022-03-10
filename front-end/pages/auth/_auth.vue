<template></template>

<script>
export default {
  name: 'AuthCallbackPage',
  async mounted() {
    const oauthToken = this.$route.query.oauth_token
    const oauthTokenSecret = localStorage.getItem('oauthTokenSecret')
    const oauthVerifier = this.$route.query.oauth_verifier

    if (oauthTokenSecret) {
      this.$axios.setHeader('Token', localStorage.getItem('secretToken'))
      const res = await this.$axios.post(`/api/req2acc`, {
        oauth_token: oauthToken,
        oauth_verifier: oauthVerifier,
        oauth_token_secret: oauthTokenSecret,
      })

      await localStorage.setItem(
        'userInfo',
        JSON.stringify({
          oauth_token: res.data.oauth_token,
          oauth_token_secret: res.data.oauth_token_secret,
          user_id: res.data.user_id,
          screen_name: res.data.screen_name,
        })
      )

      await localStorage.removeItem('oauthTokenSecret')

      window.location.href = '/'
    }
  },
}
</script>
