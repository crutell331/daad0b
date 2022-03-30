import React from 'react';
import { Box } from '@material-ui/core';
import { SenderBubble, OtherUserBubble } from '.';
import moment from 'moment';

const Messages = (props) => {
  const { messages, otherUser, user } = props;
  return (
    <Box>
      {messages.map((message, index) => {
        const time = moment(message.createdAt).format('h:mm');
        return message.senderId === user.id ? (
          <SenderBubble key={message.id} text={message.text} time={time} index={index} otherUserPhoto={otherUser.photoUrl} otherUsername={otherUser.username} read={message.read} />
        ) : (
          <OtherUserBubble
            key={message.id}
            text={message.text}
            time={time}
            otherUser={otherUser}

          />
        );
      })}
    </Box>
  );
};


export default Messages;
