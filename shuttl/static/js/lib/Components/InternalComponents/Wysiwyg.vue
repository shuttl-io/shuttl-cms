<template>
    <div id="${ block }_${self_id}_editable" class="editiable"><slot></slot></div>
</template>

<script>
    export default {
        name: "shuttl-wysiwyg",
        props: [
            "block",
            "page",
            "self_id"
        ],
        data: function() {
            return {
                recursiveSave: false
            }
        },
        methods: {
            create: function() {

            },
            getAllData: function() {
                return tinyMCE.get('{0}_{1}_editable'.format(this.block, this.self_id)).getContent();
            }
        },

        ready: function() {
            this.editor = tinymce.init({
                selector: '#{0}_{1}_editable'.format(this.block, this.self_id),
                inline: true,
                menubar: "edit insert view format table code",
                plugins: "code",
                toolbar: "undo redo | styleselect code | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent"
            });
        }
    }
</script>

<style lang="sass">
    .editiable {
        width: 100%;
        // min-height: 100px;
        border-color: rgba(0, 0, 0, 0);
        border-radius: 5px;
        border-style: dashed;
        border-width: 1px;
        padding: 0;

        box-sizing: border-box;


      -webkit-transition: border-color .3s linear; /* Saf3.2+, Chrome */
         -moz-transition: border-color .3s linear; /* FF3.7+ */
           -o-transition: border-color .3s linear; /* Opera 10.5 */
              transition: border-color .3s linear;

        &:hover {
             border-color: rgba(0, 0, 0, 1);
        }
        * {
            &:first-child {
                -webkit-margin-before: 0em;
            }

            &:last-child {
                -webkit-margin-after: 0em;
            }
        }
    }
</style>
