<template>
    <v-row
        class="pa-1"
        style="height:90%;"
        no-gutters
        fill-height
        >
        <v-col cols="12" md="4" >
            <v-list :model="xxx">
                <v-list-subheader>Параметры</v-list-subheader>
                <v-list-group
                    v-for="(item, i) in groups" :key="i"
                    :value="item.name">
                    <!-- <template v-slot:activator="{ props }"> -->
                    <template v-slot:activator="{ props }">
                        <v-list-item
                            v-bind="props"
                            :title="item.name"
                        ></v-list-item>
                    </template>

                    <v-list-item
                        v-for="(subitem) in item.items"
                        :key="subitem.id"
                        :value="subitem.id"
                        :title="subitem.name"
                    >
                        <!-- <template v-slot:prepend="{ selected }">
                            <v-list-item-action start> -->
                            <v-checkbox
                                :value="subitem.id"
                                v-model="selected"
                            ></v-checkbox>
                            <!-- </v-list-item-action>
                        </template> -->
                    </v-list-item>
                    <!-- </template> -->
                </v-list-group>
            </v-list>
        </v-col>

        <v-col cols="12" md="8">
            <!-- style="width:600px;height:250px;" -->
            <!-- style="height:90vh;" -->
            <v-card
                id="plotly_element"
            ></v-card>
        </v-col>
    </v-row>
</template>

<script>
import Plotly from "plotly.js-dist"
// const plotly_element = ref<Root>()
export default {
    name: 'PlotView',

    data() {
        return {
            // groups: ["Подшипник 1", "Подшипник 2"],
            plotly_element : null,
            selected: [],
            data_model_array : [],
            data_to_plot : [
                {
                    x: [1, 2, 3, 4],
                    y: [10, 15, 13, 17],
                    type: 'scatter'
                },
                {
                    x: [1, 2, 3, 4],
                    y: [16, 5, 11, 9],
                    type: 'scatter'
                }
            ],
            groups: [
                {
                    name:"Подшипник 1",
                    items:[
                        {id:"temperature1", name:"Температура",checked:true},
                        {id:"vibration_axial1", name:"Осевая",checked:true},
                        {id:"vibration_horizontal1", name:"Горизонтальная",checked:true},
                        {id:"vibration_vertical1", name:"Вертикальная",checked:true},
                    ]
                },
                {
                    name:"Подшипник 2",
                    items:[
                        {id:"temperature2", name:"Температура",checked:false},
                        {id:"vibration_axial2", name:"Осевая",checked:false},
                        {id:"vibration_horizontal2", name:"Горизонтальная",checked:false},
                        {id:"vibration_vertical2", name:"Вертикальная",checked:false},
                    ]
                },
                {
                    name:"Подшипник 3",
                    items:[
                        {id:"temperature3", name:"Температура",checked:false}
                    ]
                },
                {
                    name:"Подшипник 4",
                    items:[
                        {id:"temperature4", name:"Температура",checked:false}
                    ]
                },
                {
                    name:"Подшипник 5",
                    items:[
                        {id:"temperature5", name:"Температура",checked:false}
                    ]
                },
                {
                    name:"Подшипник 6",
                    items:[
                        {id:"temperature6", name:"Температура",checked:false}
                    ]
                },
                {
                    name:"Подшипник 7",
                    items:[
                        {id:"temperature7", name:"Температура",checked:true},
                        {id:"vibration_axial7", name:"Осевая",checked:true},
                        {id:"vibration_horizontal7", name:"Горизонтальная",checked:true},
                        {id:"vibration_vertical7", name:"Вертикальная",checked:true},
                    ]
                },
                {
                    name:"Подшипник 8",
                    items:[
                        {id:"temperature8", name:"Температура",checked:true},
                        {id:"vibration_axial8", name:"Осевая",checked:true},
                        {id:"vibration_horizontal8", name:"Горизонтальная",checked:true},
                        {id:"vibration_vertical8", name:"Вертикальная",checked:true},
                    ]
                },
                {
                    name:"Подшипник 9",
                    items:[
                        {id:"temperature9", name:"Температура",checked:false}
                    ]
                },
                {
                    name:"Охладитель",
                    items:[
                        {id:"oil_temperature_after", name:"Температура масла после охладителя",checked:false},
                        {id:"oil_temperature_before", name:"Температура масла до охладителя",checked:false},
                        {id:"water_temperature_after", name:"Температура воды после охладителя",checked:false},
                        {id:"water_temperature_before", name:"Температура воды до охладителя",checked:false}
                    ]
                },          
                //TODO остальное      
            ],
            name2signal : {
                "temperature1"            : "SM_Exgauster\\[3:43]",
                "vibration_axial1"        : "SM_Exgauster\\[3:14]",
                "vibration_horizontal1"   : "SM_Exgauster\\[3:12]",
                "vibration_vertical1"     : "SM_Exgauster\\[3:13]",
                "temperature2"            : "SM_Exgauster\\[3:44]",
                "vibration_axial2"        : "SM_Exgauster\\[3:17]",
                "vibration_horizontal2"   : "SM_Exgauster\\[3:15]",
                "vibration_vertical2"     : "SM_Exgauster\\[3:16]",
                "temperature3"            : "SM_Exgauster\\[3:45]",
                "temperature4"            : "SM_Exgauster\\[3:47]",
                "temperature5"            : "SM_Exgauster\\[3:48]",
                "temperature6"            : "SM_Exgauster\\[3:49]",
                "temperature7"            : "SM_Exgauster\\[3:50]",
                "vibration_axial7"        : "SM_Exgauster\\[3:20]",
                "vibration_horizontal7"   : "SM_Exgauster\\[3:18]",
                "vibration_vertical7"     : "SM_Exgauster\\[3:19]",
                "temperature8"            : "SM_Exgauster\\[3:51]",
                "vibration_axial8"        : "SM_Exgauster\\[3:23]",
                "vibration_horizontal8"   : "SM_Exgauster\\[3:21]",
                "vibration_vertical8"     : "SM_Exgauster\\[3:22]",
                "temperature9"            : "SM_Exgauster\\[3:52]",
                "oil_temperature_after"   : "SM_Exgauster\\[3:60]",
                "oil_temperature_before"  : "SM_Exgauster\\[3:59]",
                "water_temperature_after" : "SM_Exgauster\\[3:54]",
                "water_temperature_before": "SM_Exgauster\\[3:53]",
                "temperature_before"      : "SM_Exgauster\\[3:25]",
                "underpressure_before"    : "SM_Exgauster\\[3:62]",
                "gas_valve_position"      : "SM_Exgauster\\[5:13]",
                "rotor_current"           : "SM_Exgauster\\[5:9]" ,
                "rotor_voltage"           : "SM_Exgauster\\[5:11]",
                "stator_current"          : "SM_Exgauster\\[5:10]",
                "stator_voltage"          : "SM_Exgauster\\[5:12]",
                "oil_level"               : "SM_Exgauster\\[5:7]" ,
                "oil_pressure"            : "SM_Exgauster\\[5:8]" ,
            },
        }
    },

    methods: {
        update(){

            // сформировать массив данных для вывода
            // перечислить выделенные чекбоксы
            // вытащить из json ряды данных
            // цикл по выделенным чекбоксам
            this.data_to_plot = []
            for(var i = 0; i < this.selected.length; i++){ // цикл по сигналам
                const variable_name = this.selected[i];
                var signal_name = this.name2signal[variable_name];
                var series_object = {x:[], y:[], type:"scatter", name:variable_name};
                console.log("variable_name = ", variable_name,"signal_name = ", signal_name );
                for(var j = 0; j < this.data_model_array.length; j++){// цикл по оси времени
                    var x = this.data_model_array[j].message.moment;
                    var y = this.data_model_array[j].message[signal_name];
                    console.log("x = ", x, "y=", y);
                    series_object.x.push(x);
                    series_object.y.push(y);
                }
                
                this.data_to_plot.push(series_object);
            }
            
            // цикл по выделенным элементам - до

            Plotly.react(
                'plotly_element',
                this.data_to_plot
            )
        },
    },

    mounted() {
        // this.plotly_element = document.getElementById('plotly_element');
        // console.log("this.plotly_element = ", this.plotly_element);
        // Plotly.newPlot( this.plotly_element, [{
        //     x: [1, 2, 3, 4, 5],
        //     y: [1, 2, 4, 8, 16] }], {
        //     margin: { t: 0 } }
        //     );
        const date = new Date()
        date.setHours(date.getHours() - 1)
        fetch(`/api/message/?dttm_from=${date.toISOString().split(".")[0]}`)
        .then((response) => {
            return response.json();
        })
        .then((json) => {
            this.data_model_array = json;
            // console.log("this.data_model = ", this.data_model);
        })

        this.x = Plotly.newPlot( 'plotly_element',
            // [{
            // x: [1, 2, 3, 4, 5],
            // y: [1, 2, 4, 8, 16] }],
            // {
            //     margin: { t: 0 }
            // }
            );   
        this.update();
    },

    computed: {},

    watch: {
        'selected'() {
            this.update();
        }
  }
}
</script>
