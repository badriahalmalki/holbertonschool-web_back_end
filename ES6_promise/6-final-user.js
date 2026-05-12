import signUpUser from './4-user-promise';
import uploadPhoto from './5-photo-reject';

function handleProfileSignup(firstName = '', lastName = '', fileName = '') {
  return Promise.allSettled([
    signUpUser(firstName, lastName),
    uploadPhoto(fileName),
  ]).then((results) =>
    results.map((result) => {
      if (result.status === 'fulfilled') {
        return result;
      }
      return {
        status: 'rejected',
        value: result.reason.toString(),
      };
    })
  );
}

export default handleProfileSignup;
