// notifications.test.js
const { createNotification, sendNotification, formatPayload } = require('./notifications');
const db = require('../db');
const mailer = require('../mailer');

jest.mock('../db');
jest.mock('../mailer');

describe('Notification module unit tests', () => {
  test('createNotification stores a correctly shaped record', async () => {
    const feedbackId = 'fb123';
    const status = 'implemented';
    db.insert.mockResolvedValue({ id: 'notif456', ... });

    const notif = await createNotification(feedbackId, status);
    expect(db.insert).toHaveBeenCalledWith('notifications', {
      feedbackId,
      status,
      createdAt: expect.any(Date),
    });
    expect(notif.id).toBe('notif456');
  });

  test('sendNotification calls mailer with sanitized payload', async () => {
    const notif = { id: 'n1', feedbackId: 'fb1', status: 'implemented', authorEmail: '<script>@example.com' };
    mailer.send.mockResolvedValue(true);

    await sendNotification(notif);
    expect(mailer.send).toHaveBeenCalledWith({
      to: '&lt;script&gt;@example.com',
      subject: expect.stringContaining('Feedback Updated'),
      body: expect.stringContaining('implemented'),
    });
  });

  test('formatPayload escapes HTML in user‑provided fields', () => {
    const raw = { comment: '<b>Great</b>' };
    const safe = formatPayload(raw);
    expect(safe.comment).toBe('&lt;b&gt;Great&lt;/b&gt;');
  });

  test('retry logic attempts up to 3 times on failure', async () => {
    mailer.send.mockRejectedValueOnce(new Error('SMTP down'));
    mailer.send.mockResolvedValueOnce(true);

    const result = await sendNotification({ id: 'n2', authorEmail: 'user@example.com', status: 'in‑progress' });
    expect(mailer.send).toHaveBeenCalledTimes(2);
    expect(result).toBe(true);
  });

  test('createNotification throws if feedbackId missing', async () => {
    await expect(createNotification(undefined, 'implemented')).rejects.toThrow('feedbackId required');
  });
});