// Profile Page Interactions

document.addEventListener('DOMContentLoaded', function() {
  const profileEditPage = document.querySelector('[data-profile-edit]');
  
  if (profileEditPage) {
    initProfileEdit();
  }
});

/**
 * Initialize profile edit functionality
 */
function initProfileEdit() {
  const form = document.querySelector('[data-profile-form]');
  const skillsList = document.querySelector('[data-skills-list]');
  const newSkillInput = document.querySelector('[data-new-skill]');
  const addSkillButton = document.querySelector('[data-action="add-skill"]');
  const cancelButton = document.querySelector('[data-action="cancel"]');
  const saveButton = document.querySelector('[data-action="save"]');

  // Store skills in a Set for easy manipulation
  const skills = new Set(Array.from(skillsList.querySelectorAll('.profile-skill-tag')).map(el => {
    return el.textContent.replace('×', '').trim();
  }));

  /**
   * Add skill to the list
   */
  function addSkill(skillName) {
    skillName = skillName.trim();
    
    if (!skillName) return;
    if (skills.has(skillName)) {
      alert('Skill already added');
      return;
    }

    skills.add(skillName);
    renderSkills();
    newSkillInput.value = '';
  }

  /**
   * Remove skill from the list
   */
  function removeSkill(skillName) {
    skills.delete(skillName);
    renderSkills();
  }

  /**
   * Render skills list UI
   */
  function renderSkills() {
    skillsList.innerHTML = Array.from(skills).map(skill => `
      <span class="profile-skill-tag profile-skill-editable">
        ${skill}
        <button type="button" class="profile-skill-remove" data-skill="${skill}">×</button>
      </span>
    `).join('');

    // Attach event listeners to remove buttons
    skillsList.querySelectorAll('.profile-skill-remove').forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        removeSkill(this.getAttribute('data-skill'));
      });
    });

    // Update hidden input with JSON
    document.getElementById('skills_json').value = JSON.stringify(Array.from(skills));
  }

  // Event Listeners
  if (addSkillButton) {
    addSkillButton.addEventListener('click', function(e) {
      e.preventDefault();
      addSkill(newSkillInput.value);
    });
  }

  if (newSkillInput) {
    newSkillInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        addSkill(this.value);
      }
    });
  }

  // Remove skill buttons
  skillsList.querySelectorAll('.profile-skill-remove').forEach(button => {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      removeSkill(this.getAttribute('data-skill'));
    });
  });

  // Cancel button
  if (cancelButton) {
    cancelButton.addEventListener('click', function(e) {
      e.preventDefault();
      window.location.href = document.querySelector('.profile-back-button').href;
    });
  }

  // Save button
  if (saveButton) {
    saveButton.addEventListener('click', function(e) {
      e.preventDefault();
      
      // Validate form
      if (!form.role.value) {
        alert('Please select a role');
        return;
      }

      // Submit form
      form.submit();
    });
  }

  // Initialize with current skills
  renderSkills();
}
