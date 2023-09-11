'use strict';

const departments = {
    "general": {
	"science": "Science",
	"arts": "Arts",
	"commerce": "Commerce"
    },
    "ug": {
	"asp": "ASP",
	"bengali": "Bengali",
	"botany": "Botany",
	"chemistry": "Chemistry",
	"commerce": "Commerce",
	"computer science": "Computer Science",
	"economics": "Economics",
	"education": "Education",
	"electronics": "Electronic Science",
	"english": "English",
	"nutrition": "Food & Nutrition",
	"envs": "Environmental Science",
	"geography": "Geography",
	"hindi": "Hindi",
	"history": "History",
	"journalism": "Journalism & Mass Com.",
	"maths": "Mathematics",
	"philosophy": "Philosophy",
	"physical_education": "Physical Education",
	"physics": "Physics",
	"physiology": "Physiology",
	"pol_science": "Political Science",
	"sanskrit": "Sanskrit",
	"sociology": "Sociology",
	"urdu": "Urdu",
	"zoology": "Zoology",
    },
    "pg": {
	"commerce": "Commerce",
	"english": "English",
	"geography": "Geography",
	"urdu": "Urdu"
    }
};

function removeOptions(selectElement)
{
    var i, L = selectElement.options.length - 1;
    for (i = L; i >= 0; --i)
    {
	selectElement.remove(i);
    }
}
 
function update_department()
{
    var course = document.getElementById('course').value;
    var department = document.getElementById('department');
    removeOptions(department);
    for (const [key, value] of Object.entries(departments[course]))
    {
	var option = document.createElement('option');
	option.value = key;
	option.innerHTML = value;
	department.appendChild(option);
    }
}
