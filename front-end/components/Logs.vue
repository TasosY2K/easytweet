<template>
    <b-jumbotron class="jumbo" header="Logs">
        <b-button class="border-radius" variant="primary" @click="fetchLogData()">Reload</b-button>
        <br/>
        <hr/>
        <b-form-textarea class="border-radius" v-model="logContent" rows=7 ></b-form-textarea>
    </b-jumbotron>
</template>

<script>
export default {
    name: 'Logs',
    data() {
        return {
            logContent: ""
        }
    },
    methods: {
        async fetchLogData() {
            try {
                const res = await this.$axios.get(`${process.env.apiUrl}/logs`);
                this.logContent = res.data
            } catch (error) {
                this.logContent = "Could not fetch log data"
            }
        }
    },
    async mounted() {
        this.fetchLogData()
    }
}
</script>
