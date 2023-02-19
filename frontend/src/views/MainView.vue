<!-- главное окно с дашбордом агломашин и эксгаустеров -->
<template>
<!-- <v-container class="bg-surface-variant"> -->

    <!-- легенда -->
    <v-row justify="end">
        <v-col
          cols="6"
        >
            <v-sheet class="pa-2 ma-2">
                <v-icon>
                    mdi-thermometer
                </v-icon>
                Температура   
                
                <v-icon>
                    mdi-access-point
                </v-icon>
                Вибрация   
                <v-icon>
                    mdi-water
                </v-icon>
                Уровень масла   
                <v-icon color="orange">
                    mdi-square-rounded
                </v-icon>
                Предупреждение   
                <v-icon color="red">
                    mdi-square-rounded
                </v-icon>
                Опасность
            </v-sheet>
        </v-col>
    </v-row>

    <!-- список машин и эксгаустеров -->
    <v-row class="text-center" no-gutters>
        
        <v-col cols="12" md="4" class="pa-1"
            v-for="machine_item in machines_models"
            :key="machine_item.name">
            
            <!-- карточка агломашины -->
            <v-card class="pa-1">

                <!-- заголовок карточки агломашины -->
                <v-card theme="dark" color="#1F7087">
                    <v-card-title>
                        {{ machine_item.name }}
                    </v-card-title>
                </v-card>

                <!-- содержимое карточки агломашины -->
                <v-row class="mt-1">
                    <v-col
                        cols="12" md="6"
                        v-for="exhauster_item in machine_item.exhausters"
                        :key="exhausters_models[exhauster_item].name">

                        <!-- карточка эксгаустера -->
                        <v-card>

                            <!-- заголовок карточки эксгаустера -->
                            <v-card theme="dark" color="blue" class="pn-1 d-flex">
                                <!-- <v-card-title> -->
                                <p class="text-h6 ma-1 me-auto">
                                {{ exhausters_models[exhauster_item].name }}
                                </p>

                                <v-btn
                                    class="ma-1" :rounded="0"
                                    size="x-small" variant="outlined"
                                    icon="mdi-chart-line"
                                    @click="goToPlot(exhausters_models[exhauster_item].id)"
                                    ></v-btn>
                                    
                                <v-btn
                                    class="ma-1" :rounded="0"
                                    size="x-small" variant="outlined"
                                    icon="mdi-cogs"
                                    @click="goToExhauster(exhausters_models[exhauster_item].id)"
                                    ></v-btn>
                                
                                
                                <!-- </v-card-title> -->

                                
                                
                            </v-card>

                            <!-- содержимое карточки эксгаустера -->
                            <v-img src="@/assets/exhauster_small.svg"></v-img>
                            <v-list>
                                <v-list-item v-for="prediction in exhausters_models[exhauster_item].predictions" :key="prediction.bearing_num">
                                    <p> Подшипник {{prediction.bearing_num}} выйдет из строя {{getDate(prediction.expires_at)}} по причине {{prediction.reason}}. Алгоритм {{prediction.prediction_type}}</p>
                                </v-list-item>
                            </v-list>
                            <v-btn variant="tonal">
                                Сообщение в SAP
                            </v-btn>
                            
                        </v-card><!-- конец карточки эксгаустера -->
                    </v-col>
                    
                </v-row>
            </v-card><!-- конец карточки агломашины -->
        </v-col>

    </v-row>
    <!-- </v-container> -->
</template>

<script>
export default {
    name: 'MainView',

    data() {
        return {
            chosen_params:[], // список параметров, которые выбраны для отображения
            data_model : {}, // кадр состояния из кафки
            data_model_old : {}, // прошлый кадр состояния из кафки
            // модели эксгаустеров, содержащие только те поля, которые отображаются согласно настройкам
            exhausters_models : [
                {
                    "id":"0",
                    "name":"Эксгаустер У-171",
                    "predictions": [],
                },
                {
                    "id":"1",
                    "name":"Эксгаустер У-172",
                    "predictions": [],
                },
                {
                    "id":"2",
                    "name":"Эксгаустер У-173",
                    "predictions": [],
                },
                {
                    "id":"3",
                    "name":"Эксгаустер У-174",
                    "predictions": [],
                },
                {
                    "id":"4",
                    "name":"Эксгаустер У-175",
                    "predictions": [],
                },
                {
                    "id":"5",
                    "name":"Эксгаустер У-176",
                    "predictions": [],
                },
            ],


            // модели агломашин
            machines_models : [
                {
                    "name":"Агломашина №1",
                    "exhausters":[0, 1]
                },
                {
                    "name":"Агломашина №2",
                    "exhausters":[2, 3]
                },
                {
                    "name":"Агломашина №3",
                    "exhausters":[4, 5]
                },
            ]
        }
    },

    async beforeMount() {
        await this.getPrediction();
    },

    methods: {
        getDate(date_str){
            return new Date(Date.parse(date_str)).toLocaleString("ru-RU");
        },

        update(){
            // получить кадр json
            // TODO получить по API
            fetch('example_kafka.json')
            .then((response) => {
                return response.json();
            })
            .then((json) => {
                this.data_model = json[0];
                console.log("this.data_model = ", this.data_model);
            });

            // заполнить модели отображения всех эксгаустеров
            for(var i = 0; i < this.exhausters_models.length; i++){
                this.setup_display_model(i);// 
            }
        },

        async getPrediction() {
            const response = await fetch("/api/prediction/")
            for (const row of (await response.json())) {
                this.exhausters_models[row.exhauster].predictions.push(row)
            }
        },
        
        setup_display_model(i){ // заполнение модели отображения для одного эксгаустера
            this.exhausters_models[i]
        },

        goToExhauster() {
            this.$router.push({name: "ExhausterView"})
        }
    },

    mounted() {},

    computed: {},
}
</script>
