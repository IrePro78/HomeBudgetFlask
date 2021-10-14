var category_cost_list = [{
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
        text: "Transport"}, {
        id: "Inne wydatki",
        text: "Inne wydatki"},

];

var category_income_list = [{
        id: "Wynagrodzenie",
        text: "Wynagrodzenie"}, {
        id: "Zwrot podatku",
        text: "Zwrot podatku"}, {
        id: "Dodatkowy dochód",
        text: "Dodatkowy dochód"}, {
        id: "Wygrana na loterii",
        text: "Wygrana na loterii"}
];

$(function () {
        $(".form-wrap").find('#selCatCost').select2({
            data: category_cost_list
        });

    });

$(function () {
        $(".form-wrap").find('#selCatIncome').select2({
            data: category_income_list
        });
    });