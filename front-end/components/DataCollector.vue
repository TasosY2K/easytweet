<template>
    <b-jumbotron header="Data collector">
        <span>Collection name:</span>
        <b-input v-model="collectionName" type="text"></b-input>
        <span>Hashtags:</span>
        <input-tag v-model="hashTags" />
        <span>Duration start:</span>
        <date-picker v-model="datetimeStart" />
        <span>Duration end:</span>
        <date-picker v-model="datetimeEnd" />
        <br>
        <b-button variant="primary" @click="startCollecting()">{{ buttonText }}</b-button>
    </b-jumbotron>
</template>

<script>
export default {
    name: 'DataCollector',
    data() {
        return {
            buttonText: "Start",
            collectionName: null,
            hashTags: [],
            datetimeStart: null,
            datetimeEnd: null
        }
    },
    methods: {
        async startCollecting() {
            console.log(this.collectionName);
            console.log(this.hashTags);
            console.log(this.datetimeStart);
            console.log(this.datetimeEnd);
            
            const res = await this.$axios.post(`${process.env.apiUrl}/collect`, {
                collection_name: this.collectionName,
                hashtags: this.hashTags,
                datetime_start: this.datetimeStart,
                datetime_end: this.datetimeEnd
            });

            console.log(res);

            this.buttonText = "Done"   
        }
    }
}
</script>
