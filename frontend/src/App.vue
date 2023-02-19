<template>
<v-app>
    <v-app-bar app color="primary" dark clipped-left>

        <!-- логотип -->
        <!-- <v-icon> -->
            <v-img src="favicon.png" max-width="50"></v-img>
        <!-- </v-icon> -->
        <!-- <v-divider class="mx-2" vertical></v-divider> -->
        <v-app-bar-title justify-start>
            <h2 justify-start>{{ "FoxControl" }}</h2>
        </v-app-bar-title>
        
        <v-spacer></v-spacer>

        <div justify-end class="pa-0 ma-0 fill-height">
            <v-container justify-end class="pa-0 ma-0 fill-height">

                <!-- <v-spacer></v-spacer> -->

                <v-divider vertical class="mx-2 fill-height"></v-divider>

                <v-avatar color="white">
                    <v-icon color="primary">
                        <!-- mdi-account-multiple -->
                        mdi-account-circle
                    </v-icon>
                </v-avatar>
                
                <div class="px-4">
                    <span class="text-2xl text-white font-semibold">
                        Имя пользователя
                    </span>
                </div>
                <v-divider inset vertical class="mx-2"></v-divider>

                <!-- <v-btn outlined @click="logout"> Выход </v-btn> -->

            </v-container>
        </div>

    </v-app-bar>

    <!--  -->
    <!-- :mini-variant.sync="mini" -->

    <!-- Sizes your content based upon application components -->
    <!-- <v-main style="height: 100vh;"> -->
    <v-main style="height: 100vh;">
        <!-- <v-container fluid fill-height> -->
            <!-- If using vue-router -->
            <router-view></router-view>
        <!-- </v-container> -->
    </v-main>
</v-app>
</template>

<script>
export default {
  data() {
    return {

    }
  },

  methods: {},

  mounted() {},

  computed: {},

}
</script>
