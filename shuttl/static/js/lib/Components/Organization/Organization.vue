<template>
	<div class="organization" v-bind:class="{ 'stripe': isOdd }">
		<div class="cell check">
			<input type="checkbox" name="selector" v-on:click="selected"/>
		</div>

		<div class="cell input">
			<a href="//${organization.name}.${organization.reseller._url}" v-show="!shouldEdit">${ organization.name }</a>
			<input type="text" v-model="organization.name" v-show="shouldEdit" v-on:keyup.enter="edit"/>
		</div>

		<div class="cell edit">
			<button v-on:click.prevent="edit" class="btn">${buttonText}</button>
		</div>

		<div class="cell delete">
			<button v-on:click.prevent="delete(true)" class="btn danger">Delete</button>
		</div>

	</div>
</template>

<script>
	export default {
		name: "shuttl-organization",
		data: function() {
			return {
				shouldEdit: false,
				buttonText: "Edit",
				originalName: "",
				selectedIndex: -1
			}
		},

		computed: {
			isOdd: function() {
				return this.index % 2 != 0;
			}
		},

		props : [
			"organization",
			"index"
		],

		methods: {
			edit: function() {
				if(this.shouldEdit) {
					var formData = new FormData();
					formData.append("name", this.organization.name);
					this.$http.patch("/organization/{0}".format(this.organization.id), formData).then((response)=> {
						this.shouldEdit = false;
						this.buttonText = "Edit"
					}, (response) => {
						console.log("An error occured. Code: {0}".format(response.status));
						this.organization.id = this.originalName;

					});
				}
				else {
					this.buttonText = "Save";
					this.shouldEdit = true;
				}
			},

			selected: function() {
				let self = this;
				if (self.selectedIndex == -1){
		       		self.$dispatch("select", self);
				}
				else {
					self.$dispatch("remove", self.selectedIndex);
					self.selectedIndex = -1;
				}
		    },

		    setSelectedIndex: function(number) {
		    	this.selectedIndex = number;
		    },

		    delete: function(confirm) {
		    	this.$http.delete("/organization/{0}".format(this.organization.id)).then((response)=>{
		    		this.$dispatch("deleted", this.index);
		    	}, (response) => {
		    		console.log("An Error Occured while deleting the organization.");
		    		alert("An Error Occured while deleting the organization. Please Try again.");
		    	});
		    }
		},

		ready: function() {
		 	this.originalName = this.organization.id;
		}
	}
</script>

<style lang="sass" scoped>
	.organization {
		display: flex;
		display: -webkit-flex;

		&.stripe {
			background-color: #EDEBD7;
		}


		.cell {
			padding: 5px;
			height: 25px;
			p {
				margin: 0;
			}

			&.edit {
				display: flex;
				display: -webkit-flex;
				justify-content: center;
				padding: 5px 0;
				width: 100px;
				button {
					width: 75px;
					height: 22px;
				}
			}

			&.input {
				min-width: 400px;
			}
		}
	}
</style>
