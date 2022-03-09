<template>
    <b-jumbotron class="jumbo" header="Monitor">
        <b-button class="border-radius" variant="primary" @click="fetchThreads()">Reload</b-button>&nbsp;
        <span>{{ spanText }}</span>
        <hr/>
        <b-table v-if="threadsRunning" striped hover :items="threads"></b-table>
    </b-jumbotron>
</template>

<script>
export default {
    name: 'Monitor',
    data() {
        return {
            spanText: "Loading running threads...",
            threadsRunning: false,
            threads: []
        }
    },
    methods: {
        async fetchThreads() {
            this.spanText = "Loading running threads..."
            try {
                const res = await this.$axios.get(`${process.env.apiUrl}/monitor`);
                if (res.status == 200) {
                    this.threadsRunning = true
                    this.threads = res.data;
                    this.spanText = "Threads loaded"   
                } else {
                    this.threads = []
                    this.threadsRunning = false
                    this.spanText = "No running threads found"
                }
            } catch (error) {
                this.threads = []
                this.threadsRunning = false
                this.spanText = "No running threads found"   
            }
        }
    },
    mounted() {
        this.fetchThreads()
    }
}
</script>
