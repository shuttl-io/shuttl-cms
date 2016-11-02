<template>
    <div id="${ self_id }_obtained"><slot></slot></div>
</template>

<script>
    import saveLevel from "../../SaveLevel.js";
    export default {
        name: "shuttl-obtain",
        props: [
            "self_id"
        ],
        data: function() {
            return {
                recursiveSave: true
            }
        },
        methods: {
            create: function() {

            },
            getAllData: function() {
                return saveLevel(this);
            }
        },

        ready: function() {
            window.globals.push(this);
        }
    }
</script>
