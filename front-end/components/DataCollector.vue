<template>
    <b-jumbotron header="Data collector" class="center">
        <p>collect</p>
        <b-button variant="primary" @click="logout()">Logout</b-button>
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
    name: 'LoginWithTwitter',
    methods: {
        logout() {
            localStorage.removeItem("userInfo");
            window.location.href = "/";
        }
    }
}
</script>
