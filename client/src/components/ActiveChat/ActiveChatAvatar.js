import React from "react";
import { Box, Badge, Avatar } from "@material-ui/core";

import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  profilePic: {
    height: 44,
    width: 44,
  },
  activeChatPic:{
    height: 14,
    width: 14,
  },
  badge: {
    height: 13,
    width: 13,
    borderRadius: "50%",
    border: "2px solid white",
    backgroundColor: "#D0DAE9",
  }
}));


const ActiveChatAvatar = ({ photoUrl, otherUsername }) => {
  const classes = useStyles();

  return (
    <Box className="">
      <Badge
        classes={{ badge: `${classes.badge}` }}
        anchorOrigin={{ horizontal: "right", vertical: "bottom" }}
        overlap="circular"
      >
        <Avatar alt={otherUsername} src={photoUrl} className={classes.activeChatPic} />
      </Badge>
    </Box>
  );
};

export default ActiveChatAvatar;
