<template>
	<div class="container">
		<div class="orgAdd">
			<div class="inputForm">
				<input type="text" name="name" v-model="organization.name" placeholder="New Organization" v-on:keyup.enter="addOrg" />
			</div>
			<div class="inputAdd">
				<button v-on:click.prevent="addOrg" class="btn info" v-bind:class="{ 'disabled': canAdd }">Add</button>
			</div>
		</div>
		<div class="orgList">
			<shuttl-organization v-for="organization in organizations" 
				:organization="organization"
				:index="$index">
			</shuttl-organization>
		</div>

		<div class="btn-group">
			<button value="delete" name="delete" class="btn danger" v-on:click.prevent="deleteSelected" v-if="!isDisabled">
					Delete Organization(s)
			</button>
		</div>
	</div>

</template>

<script>
	import Organization from "./Organization.vue";
	
	export default {
		name: "shuttl-organizations",

		data: function() {
			return {
				organizations: [],
				organization: { name: ""},
				selectedOrgs: []
			}
		},

		computed: {
			canAdd: function() {
				return this.organization.name === "";
			},

			isDisabled: function() {
				return this.selectedOrgs.length == 0;
			}
		},

		components: {
    		"shuttl-organization": Organization
    	},

		methods: {
			fetchOrgs: function() {
				this.$http.get("/organization/").then((response) => {
					if (response.status == 200) {
						this.organizations = response.data;
					}
					else {
						console.log("An error occured. Code: {0}".format(response.status));
					}
				}, (response) => {
					console.log("An error occured. Code: {0}".format(response.status));
				});
			},

			addOrg: function() {
				if(this.canAdd) return;
				var formData = new FormData();
				formData.append("name", this.organization.name)
				this.$http.post("/organization/", formData).then((response) => {
					if (response.status == 201) {
						this.organizations.push(response.data);
						this.organization.name = "";
					}
				}, (response) => {
					if (response.status == 409) {
						alert("An organization with that name already exists. Choose a new name and try again.");
					}
					console.log("An error Occured: {0}".format(response.status));
					alert("An error occured while create the new Organization, Please try again.");
				});
			},

			deleteSelected: function() {
				this.selectedOrgs.forEach((element, index, array) => {
					element.delete(false);
				});
				this.selectedOrgs = [];
			}
		},

		ready: function() {
		  // When the application loads, we want to call the method that initializes
		  // some data
		  this.fetchOrgs();
		},

		events: {
			"select": function(selected) {
				this.selectedOrgs.push(selected);
				selected.setSelectedIndex(this.selectedOrgs.length-1);
			},

			"remove": function(ndx) {
				this.selectedOrgs.splice(ndx, 1);
			},

			"deleted": function(ndx) {
				this.organizations.splice(ndx, 1);
			}
		}
	}
</script>

<style lang="sass">
	.container {
		.orgList {
			border-style: solid;
			border-color: darken(#EDEBD7, 10%);
			border-width: 1px;
		}
		@mixin btnColor($color){
			background-color: $color;
			&.disabled {
				background-color: lighten($color, 10%);
			}
		}
		.btn {
			$background-color: #5cb85c;
			@include btnColor($background-color);
			&.danger{
				@include btnColor(#ea3424);
			}
			&.info {
				@include btnColor(#4EA2BE);
			}
			border: 1px solid transparent;
			border-radius: 4px;
			color: white;

			&.disabled {
				cursor: not-allowed;
			}
			
		}
		width: 40em;
		margin: 0 auto;

		.btn-group {
			width: 84%;
			display: flex;
			display: -webkit-flex;
			justify-content: center;
		}
	}
	.orgAdd {
		width: 84%;
		display: flex;
		display: -webkit-flex;
		justify-content: center;
		margin-bottom: 30px;
		.inputAdd {
			margin-left: 20px;
		}
	}
</style>