let techMajorRadio = document.getElementById("radio_one");
let econMajorRadio = document.getElementById("radio_two");
let techMajorFaculties = document.getElementById("tech_faculties");
let econMajorFaculties = document.getElementById("econ_faculties");

console.log(techMajorFaculties)
console.log(econMajorFaculties)



function changeTechVisibility() {
    let techMajorFacultiesDisplayStatus = techMajorFaculties.style.display;
    
    if (techMajorFacultiesDisplayStatus == 'none') {
        techMajorFaculties.style.display = 'block';
        econMajorFaculties.style.display = 'none';
    }
    // alert(techMajorFacultiesDisplayStatus)
} 
function changeEconVisibility() {
    let econMajorFacultiesDisplayStatus = econMajorFaculties.style.display;
    
    if (econMajorFacultiesDisplayStatus == 'none') {
        techMajorFaculties.style.display = 'none';
        econMajorFaculties.style.display = 'block';
    }
} 