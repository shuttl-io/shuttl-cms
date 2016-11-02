<template>
    <a href="#" v-on:click.prevent="create">${template.name}</a>
</template>

<script>
    export default {
        name: "shuttl-webpage",
        props: [
            "template"
        ],
        methods: {
            create: function() {
                this.$dispatch("templateSelected", this.template);
            }
        }
    }
</script>

<style lang="sass">

</style>
