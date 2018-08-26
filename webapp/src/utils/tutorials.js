const hasCompletedTutorial = (ls, name) =>
  ls.completedTutorials[name] || false;


const completeTutorial = (ls, name) => {
  if (ls.completedTutorials[name]) return;
  const d = { ...ls.completedTutorials, [name]: true };
  ls.set('completedTutorials', d);
};

export {
  hasCompletedTutorial,
  completeTutorial,
};
