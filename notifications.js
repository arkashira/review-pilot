// Add event listener for status changes
const { EventEmitter } = require('events');
const Notification = require('./models/Notification');

class NotificationService extends EventEmitter {
  constructor() {
    super();
    this.init();
  }

  init() {
    // Listen for feedback status updates
    this.on('feedback.status.updated', async (data) => {
      const { feedbackId, oldStatus, newStatus, userId } = data;
      
      // Create progress notification
      const notification = new Notification({
        type: 'progress_update',
        entityId: feedbackId,
        userId,
        message: `Feedback #${feedbackId} status changed from ${oldStatus} to ${newStatus}`,
        metadata: {
          oldStatus,
          newStatus,
          timestamp: new Date().toISOString()
        }
      });
      
      await notification.save();
      this.emit('notification.created', notification);
    });
  }
}

module.exports = new NotificationService();