// Add status update endpoint
const express = require('express');
const router = express.Router();
const notificationService = require('../notifications');

router.patch('/:id/status', async (req, res) => {
  const { id } = req.params;
  const { status } = req.body;
  
  // Get current feedback status
  const feedback = await getFeedbackById(id);
  const oldStatus = feedback.status;
  
  // Update status
  await updateFeedbackStatus(id, status);
  
  // Trigger notification
  notificationService.emit('feedback.status.updated', {
    feedbackId: id,
    oldStatus,
    newStatus: status,
    userId: req.user.id
  });
  
  res.status(200).json({ 
    message: `Feedback #${id} status updated to ${status}`,
    status: 'success'
  });
});