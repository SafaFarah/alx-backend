import kue from 'kue';
import { expect } from 'chai';
import createPushNotificationsJobs from './8-job.js';

const queue = kue.createQueue();

describe('createPushNotificationsJobs', () => {
  before((done) => {
    queue.testMode.enter();
    done();
  });

  after((done) => {
    queue.testMode.clear();
    queue.testMode.exit();
    done();
  });

  it('should throw an error if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs({}, queue)).to.throw(Error, 'Jobs is not an array');
  });

  it('should create jobs in the queue', (done) => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'This is the code 1234 to verify your account' },
      { phoneNumber: '4153518781', message: 'This is the code 4562 to verify your account' },
    ];

    createPushNotificationsJobs(jobs, queue);

    // Validate jobs in the queue
    const jobIds = queue.testMode.jobs;
    expect(jobIds).to.have.lengthOf(2);
    expect(jobIds[0].data).to.deep.include(jobs[0]);
    expect(jobIds[1].data).to.deep.include(jobs[1]);

    done();
  });
});
