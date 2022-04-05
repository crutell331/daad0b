import React from 'react';
import { Box } from '@material-ui/core';
import { SenderBubble, OtherUserBubble } from '.';
import moment from 'moment';

const Messages = (props) => {
  const { messages, otherUser, user, lastReadMessage } = props;
  return (
    <Box>
      {messages.map((message) => {
        const time = moment(message.createdAt).format('h:mm');

        return message.senderId === user.id ? (
          <SenderBubble key={message.id} text={message.text} time={time} otherUserPhoto={otherUser.photoUrl} otherUserName={otherUser.username} read={lastReadMessage === message.id}/>
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
