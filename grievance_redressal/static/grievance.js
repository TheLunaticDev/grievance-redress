'use strict';

const departments = {
    "General": {
	"Science": "Science",
	"Arts": "Arts",
	"Commerce": "Commerce"
    },
    "UG": {
	"ASP": "ASP",
	"Bengali": "Bengali",
	"Botany": "Botany",
	"Chemistry": "Chemistry",
	"Commerce": "Commerce",
	"Computer Science": "Computer Science",
	"Economics": "Economics",
	"Education": "Education",
	"Electronic Science": "Electronic Science",
	"English": "English",
	"Food & Nutrition": "Food & Nutrition",
	"Environmental Science": "Environmental Science",
	"Geography": "Geography",
	"Hindi": "Hindi",
	"History": "History",
	"Journalism & Mass Com.": "Journalism & Mass Com.",
	"Mathematics": "Mathematics",
	"Philosophy": "Philosophy",
	"Physical Education": "Physical Education",
	"Physics": "Physics",
	"Physiology": "Physiology",
	"Political Science": "Political Science",
	"Sanskrit": "Sanskrit",
	"Sociology": "Sociology",
	"Urdu": "Urdu",
	"Zoology": "Zoology",
    },
    "PG": {
	"Commerce": "Commerce",
	"English": "English",
	"Geography": "Geography",
	"Urdu": "Urdu"
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
