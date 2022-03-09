<template>
    <b-jumbotron class="jumbo" header="Data collector">
        <span>Collection name:</span>
        <b-input class="border-radius" v-model="collectionName" type="text" @input="validate()" ></b-input>
        <span>Hashtags:</span>
        <input-tag class="border-radius" v-model="hashTags" @input="validate()" />
        <span>Duration end:</span>
        <date-picker class="border-radius" v-model="datetimeEnd" @input="validate()" />
        <br>
        <b-button class="border-radius" :disabled="disabled" variant="primary" @click="startCollecting()">{{ buttonText }}</b-button>
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
            datetimeEnd: null,
            disabled: true,
        }
    },
    methods: {
        validate() {
            if (!this.collectionName || !this.datetimeEnd || this.hashTags.length < 0) {
                this.disabled = true
            } else {
                this.disabled = false
            }
        },
        async startCollecting() {
            try {
                const res = await this.$axios.post(`${process.env.apiUrl}/collect`, {
                    collection_name: this.collectionName,
                    hashtags: this.hashTags,
                    datetime_end: this.datetimeEnd
                });

                this.buttonText = res.data;
            } catch (error) {
                alert(error)
            }
        }
    }
}
</script>
