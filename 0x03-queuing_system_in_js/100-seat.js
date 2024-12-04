import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

const app = express();
const PORT = 1245;

const Client = redis.createClient();
const setAsync = promisify(Client.set).bind(Client);
const getAsync = promisify(Client.get).bind(Client);

// Initialize Kue queue
const queue = kue.createQueue();

const initialAvailableSeats = 50;
Client.set('available_seats', initialAvailableSeats);

let reservationEnabled = true;

function reserveSeat(number) {
    Client.set('available_seats', number);
}

const getCurrentAvailableSeats = async () => {
    const seats = await getAsync('available_seats');
    return Number(seats);
};

app.get('/available_seats', async (req, res) => {
    const availableSeats = await getCurrentAvailableSeats();
    res.send({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', async (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: 'Reservations are blocked' });
    }

    const job = queue.create('reserve_seat').save((err) => {
        if (!err) {
            return res.json({ status: 'Reservation in process' });
        }
        return res.json({ status: 'Reservation failed' });
    });
    job.on('complete', () => {
       console.log(`Seat reservation job ${job.id} completed`);
    }).on('failed', (errorMessage) => {
      console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', (req, res) => {
    queue.process('reserve_seat', async (job, done) => {
        try {
            const availableSeats = await getCurrentAvailableSeats();
            const newAvailableSeats = availableSeats - 1;
            reserveSeat(newAvailableSeats);
            if (newAvailableSeats === 0) {
                reservationEnabled = false;
            }
            done();
        } catch (error) {
            done(new Error('Not enough seats available'));
        }
    });
    res.json({ status: 'Queue processing' });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
