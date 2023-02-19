<template>
<!-- <v-container style="height: 90vh;"> -->
<v-row
    style="width:80%;"
    no-gutters
>
    <v-col
        cols="12"
        sm="12"
        md="12"
        class="ps-2"
        no-gutters
    >
        <!-- <v-img id="svgimage"
            src="exhauster.svg"
        >
        </v-img> -->

        <object
            @load="onSvgLoaded"
            id="svgobject"
            data="exhauster.svg"
            type="image/svg+xml"
        ></object>

        <!-- <svg
            
        ></svg> -->

    </v-col>
</v-row>
    <!-- <v-progress-linear
        :v-model="50"
        height="25"
        x="100px"
        y="100px"
        >
        50%
    </v-progress-linear> -->
<!-- </v-container> -->
</template>

<script>
import { SVG, Text } from "@svgdotjs/svg.js"
import exhauster_svg_url from "@/assets/exhauster.svg"
export default {
    name: 'ExhausterView',

    props: {
        exhauster_id:String,
    },

    data() {
        return {
            xxx : 0,
            sample_text_label : null,
            svgobject : null,
            data_model : {},
            exhauster_svg: exhauster_svg_url
        }
    },

    methods: {
        onSvgLoaded(){
            console.log("onSvgLoaded():");
            this.svgobject = document.getElementById("svgobject").contentDocument;
            console.log("svg = ", this.svgobject);
            // this.sample_text_label = this.svgobject.getElementById('text787');
            // this.sample_text_label = $('#tspan785');
            // console.log("svg_text_label = ", this.sample_text_label);
            // this.sample_text_label.textContent = this.xxx;

            console.log("2 this.exhauster_id = ", this.exhauster_id);
            console.log("2 $route.params.exhauster_id = ", this.$route.params.exhauster_id);
            console.log("2 props.exhauster_id = ", this.$props.exhauster_id);
        },

        updateSVG(){ // перерисовка SVG при получении очередной телеметрии
            // TODO переделать на табличную загрузку, слишком топорно

            // формат: [сигнал, id_текста, сигнал_max1, сигнал_min1, сигнал_max2, сигнал_min2]
            // id прямоугольника, который нужно анимировать, составляется как "rect_"+id_текста
            var signal2label = [
                ["SM_Exgauster\\[3:43]","temperature1"            , "SM_Exgauster\\[3:99]",     "SM_Exgauster\\[3:108]", "SM_Exgauster\\[3:117]", "SM_Exgauster\\[3:126]"],
                ["SM_Exgauster\\[3:14]","vibration_axial1"        , "SM_Exgauster\\[3:185]",	"SM_Exgauster\\[3:197]", "SM_Exgauster\\[3:209]", "SM_Exgauster\\[3:221]"],
                ["SM_Exgauster\\[3:12]","vibration_horizontal1"   , "SM_Exgauster\\[3:183]",	"SM_Exgauster\\[3:195]", "SM_Exgauster\\[3:207]", "SM_Exgauster\\[3:219]"],
                ["SM_Exgauster\\[3:13]","vibration_vertical1"     , "SM_Exgauster\\[3:184]",	"SM_Exgauster\\[3:196]", "SM_Exgauster\\[3:208]", "SM_Exgauster\\[3:220]"],
                ["SM_Exgauster\\[3:44]","temperature2"            , "SM_Exgauster\\[3:100]",	"SM_Exgauster\\[3:109]", "SM_Exgauster\\[3:118]", "SM_Exgauster\\[3:127]"],
                ["SM_Exgauster\\[3:17]","vibration_axial2"        , "SM_Exgauster\\[3:188]",	"SM_Exgauster\\[3:200]", "SM_Exgauster\\[3:212]", "SM_Exgauster\\[3:224]"],
                ["SM_Exgauster\\[3:15]","vibration_horizontal2"   , "SM_Exgauster\\[3:186]",	"SM_Exgauster\\[3:198]", "SM_Exgauster\\[3:210]", "SM_Exgauster\\[3:222]"],
                ["SM_Exgauster\\[3:16]","vibration_vertical2"     , "SM_Exgauster\\[3:187]",	"SM_Exgauster\\[3:199]", "SM_Exgauster\\[3:211]", "SM_Exgauster\\[3:223]"],
                ["SM_Exgauster\\[3:45]","temperature3"            , "SM_Exgauster\\[3:101]",	"SM_Exgauster\\[3:110]", "SM_Exgauster\\[3:119]", "SM_Exgauster\\[3:128]"],
                ["SM_Exgauster\\[3:47]","temperature4"            , "SM_Exgauster\\[3:102]",	"SM_Exgauster\\[3:111]", "SM_Exgauster\\[3:120]", "SM_Exgauster\\[3:129]"],
                ["SM_Exgauster\\[3:48]","temperature5"            , "SM_Exgauster\\[3:103]",	"SM_Exgauster\\[3:112]", "SM_Exgauster\\[3:121]", "SM_Exgauster\\[3:130]"],
                ["SM_Exgauster\\[3:49]","temperature6"            , "SM_Exgauster\\[3:104]",	"SM_Exgauster\\[3:113]", "SM_Exgauster\\[3:122]", "SM_Exgauster\\[3:131]"],
                ["SM_Exgauster\\[3:50]","temperature7"            , "SM_Exgauster\\[3:105]",	"SM_Exgauster\\[3:114]", "SM_Exgauster\\[3:123]", "SM_Exgauster\\[3:132]"],
                ["SM_Exgauster\\[3:20]","vibration_axial7"        , "SM_Exgauster\\[3:191]",	"SM_Exgauster\\[3:203]", "SM_Exgauster\\[3:215]", "SM_Exgauster\\[3:227]"],
                ["SM_Exgauster\\[3:18]","vibration_horizontal7"   , "SM_Exgauster\\[3:189]",	"SM_Exgauster\\[3:201]", "SM_Exgauster\\[3:213]", "SM_Exgauster\\[3:225]"],
                ["SM_Exgauster\\[3:19]","vibration_vertical7"     , "SM_Exgauster\\[3:190]",	"SM_Exgauster\\[3:202]", "SM_Exgauster\\[3:214]", "SM_Exgauster\\[3:226]"],
                ["SM_Exgauster\\[3:51]","temperature8"            , "SM_Exgauster\\[3:106]",	"SM_Exgauster\\[3:115]", "SM_Exgauster\\[3:124]", "SM_Exgauster\\[3:133]"],
                ["SM_Exgauster\\[3:23]","vibration_axial8"        , "SM_Exgauster\\[3:194]",	"SM_Exgauster\\[3:206]", "SM_Exgauster\\[3:218]", "SM_Exgauster\\[3:230]"],
                ["SM_Exgauster\\[3:21]","vibration_horizontal8"   , "SM_Exgauster\\[3:192]",	"SM_Exgauster\\[3:204]", "SM_Exgauster\\[3:216]", "SM_Exgauster\\[3:228]"],
                ["SM_Exgauster\\[3:22]","vibration_vertical8"     , "SM_Exgauster\\[3:193]",	"SM_Exgauster\\[3:205]", "SM_Exgauster\\[3:217]", "SM_Exgauster\\[3:229]"],
                ["SM_Exgauster\\[3:52]","temperature9"            , "SM_Exgauster\\[3:107]",	"SM_Exgauster\\[3:116]", "SM_Exgauster\\[3:125]", "SM_Exgauster\\[3:134]"],
                ["SM_Exgauster\\[3:60]","oil_temperature_after"   , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[3:59]","oil_temperature_before"  , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[3:54]","water_temperature_after" , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[3:53]","water_temperature_before", null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[3:25]","temperature_before"      , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[3:62]","underpressure_before"    , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[5:13]","gas_valve_position"      , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[5:9]" ,"rotor_current"           , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[5:11]","rotor_voltage"           , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[5:10]","stator_current"          , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[5:12]","stator_voltage"          , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[5:7]" ,"oil_level"               , null], // для значения не предусмотрена сигнализация min/max
                ["SM_Exgauster\\[5:8]" ,"oil_pressure"            , null], // для значения не предусмотрена сигнализация min/max
            ];

            console.log("this.data_model3 = ", this.data_model);
            for(var pair of signal2label){
                // console.log("pair = ", pair);
                // console.log("this.data_model.Message.moment = ", this.data_model.Message[pair[0]]);
                const label_name = pair[1];
                // console.log("label_name = ", label_name);
                var label_element = this.svgobject.getElementById(label_name);
                // console.log("label_element = ", label_element);
                const value = this.data_model[pair[0]]
                label_element.textContent = value.toFixed(2);

                //TODO убрать
                // this.data_model[pair[0]] += 5.0;

                // включение или отключение анимации
                if(pair[2]==null){
                    continue;
                }

                const value_alarm_max = this.data_model[pair[2]];
                const value_alarm_min = this.data_model[pair[3]];
                const value_warning_max = this.data_model[pair[4]];
                const value_warning_min = this.data_model[pair[5]];
                console.log("min max = ", value_alarm_max, value_alarm_min);
                var rect_element = this.svgobject.getElementById("rect_"+pair[1]);
                var animation = rect_element.getElementsByTagName('animate')[0];

                if(value >= value_alarm_max || value <= value_alarm_min){ // тревога
                    rect_element.style.fill = "red";// цвет
                    // включить мигание
                    animation.setAttribute("repeatCount","indefinite");
                }
                else if(value >= value_warning_max || value <= value_warning_min){ // предупреждение
                    rect_element.style.fill = "orange";// цвет
                    // выключить мигание
                    animation.setAttribute("repeatCount","0");
                }
                else{
                    rect_element.style.fill = "gray";// цвет
                    animation.setAttribute("repeatCount","0");
                    // выключить мигание
                }
                
                // rect_element.style.fill = "red"; // РАБОТАЕТ
            }
        },

        fetchLatestMessage() {
            fetch('/api/message/latest/')
            .then((response) => {
                return response.json();
            })
            .then((json) => {
                this.data_model = json.message;
                // console.log("this.data_model = ", this.data_model);
            })
            .then(()=>{
                // console.log("this.data_model2 = ", this.data_model);
                this.updateSVG();
            });
        }
    },


    mounted() {
        console.log("1 this.exhauster_id = ", this.exhauster_id);
        console.log("1 $route.params.exhauster_id = ", this.$route.params.exhauster_id);
        console.log("1 props.exhauster_id = ", this.$props.exhauster_id);

        // const dataObjectFromFile = require('example_kafka.json');
        this.fetchLatestMessage();

        setInterval(()=>{
            // for(var [key, ] of this.data_model.Message){
            //     this.data_model.Message[key] += 1;
            // }
            // this.xxx += 1;
            // this.sample_text_label.textContent = this.xxx;
            this.fetchLatestMessage();
        }, 15000);

        // this.svg = document.getElementById("svg2106").contentDocument;
        // console.log("svg = ", this.svg);
    },

    computed: {},
}
</script>
