// Código de Typed.js
const selectTyped = document.querySelector('.typed');
if (selectTyped) {
  let typed_strings = selectTyped.getAttribute('data-typed-items');
  typed_strings = typed_strings.split(',');
  new Typed('.typed', {
    strings: typed_strings,
    loop: true,
    typeSpeed: 20,
    backSpeed: 50,
    backDelay: 2000
  });
}

// Código de las barras de progreso
document.addEventListener("DOMContentLoaded", function() {
  // Define skills and percentages
  const skills = [
    { name: 'Electronica', percentage: 90 },
    { name: 'Python', percentage: 90 },
    { name: 'Inglés', percentage: 100 },
    { name: 'Desarrollo Web', percentage: 80 },
    { name: 'Linux', percentage: 85 },
  ];

  // Get the container where the skill bars will go
  const skillsList = document.getElementById('skills-list');

  // Loop through skills and create progress bars
  skills.forEach(skill => {
    // Create skill element
    const skillDiv = document.createElement('div');
    skillDiv.classList.add('progress');
    
    // Create skill title and value
    const skillTitle = document.createElement('span');
    skillTitle.classList.add('skill');
    skillTitle.innerHTML = `<span>${skill.name}</span> <i class="val">${skill.percentage}%</i>`;
    
    // Create progress bar wrapper
    const progressBarWrap = document.createElement('div');
    progressBarWrap.classList.add('progress-bar-wrap');

    // Create the actual progress bar
    const progressBar = document.createElement('div');
    progressBar.classList.add('progress-bar');
    progressBar.setAttribute('role', 'progressbar');
    progressBar.setAttribute('aria-valuenow', skill.percentage);
    progressBar.setAttribute('aria-valuemin', '0');
    progressBar.setAttribute('aria-valuemax', '100');
    progressBar.style.width = `${skill.percentage}%`; // Set the width based on percentage

    // Append everything to the DOM
    progressBarWrap.appendChild(progressBar);
    skillDiv.appendChild(skillTitle);
    skillDiv.appendChild(progressBarWrap);
    skillsList.appendChild(skillDiv);
  });
});
