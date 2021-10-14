var category_list = [{
        id: "Jedzenie",
        text: "Jedzenie"}, {
        id: "Mieszkanie",
        text: "Mieszkanie"}, {
        id: "Inne opłaty i rachunki",
        text: "Zdrowie, higiena i chemia"}, {
        id: "Ubranie",
        text: "Ubranie"}, {
        id: "Relaks",
        text: "Relaks"}, {
        id: "Transport",
        text: "Trnsport"}, {
        id: "Inne wydatki",
        text:"Inne wydatki"}
];

$(function () {


        $(".form-wrap").find('#selectCategory').select2({
            data: category_list
        });
    });

