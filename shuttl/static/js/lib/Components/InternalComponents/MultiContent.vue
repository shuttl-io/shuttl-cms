<template>
    <div id="${ self_id }_multiBlock" class="multicontent editiable">
    <button v-on:click.prevent="appendAfter" class="add hover-show"></button>
    <button v-on:click.prevent="remove" class="remove hover-show"></button>
        <slot></slot>
    </div>
</template>

<script>
    import saveLevel from "./../../SaveLevel.js";

    export default {
        name: "shuttl-multiitem",
        props: [
            "self_id",
            "index",
            "owner",
            "block"
        ],
        data: function() {
            return {
                recursiveSave: true,
                url: null
            }
        },
        methods: {
            _handleSuccess: function(response) {
                if (response.status == 200) {
                    parent.internalNav.save();
                }
                else {
                    console.log("An error occured. Code: {0}".format(response.status));
                }
            },
            _handleFail: function(response){
                console.log("An error occured. Code: {0}".format(response.status));
            },
            appendAfter: function() {
                this.$http.post(this.url).then((response) => {
                    this._handleSuccess(response);
                }, (response) => {
                    this._handleFail(response);
                });
            },
            getAllData: function() {
                return saveLevel(this);
            },
            remove: function() {
                 this.$http.delete(this.url).then((response) => {
                    this._handleSuccess(response);
                }, (response) => {
                    this._handleFail(response);
                });
            }
        },

        ready: function() {
            this.url = "/website/{0}/page/{1}/multiBlocks/{2}/{3}".format(window.parent.website_id, window.parent.page_id, this.owner, this.index)
        },
    }
</script>

<style lang="sass">
    .editiable {
        $size: 16px;
        position: relative;
        .add {
            left: 0;
                background: url(//shuttl.io/static/img/plus.png) no-repeat;

        }
        .remove {
            left: $size+10;
            background: url(//shuttl.io/static/img/minus.png) no-repeat;
        }
        .hover-show {
            background-color: transparent;
            border: none;
            width: $size;
            height: $size;
            text-indent:-9999px;
            position: absolute;
            cursor: pointer;
            display: none;
            background-position: center;
            background-size: 100% 100%;
        }

        &:hover {
            .hover-show {
                display: inline-block;
            }
        }
    }
</style>
