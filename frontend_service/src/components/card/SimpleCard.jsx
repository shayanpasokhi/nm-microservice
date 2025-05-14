import Card from "@mui/material/Card";
import { CardActionArea } from "@mui/material";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";

const SimpleCard = ({ icon, title, des }) => {
  return (
    <Card
      variant="outlined"
      sx={{
        minHeight: 200,
        height: 1,
        display: "flex",
        justifyContent: "center",
        width: 150,
        minWidth: 150,
        mb: 1,
        borderRadius: 5,
        borderColor: "#bbb",
        mr: 2,
      }}
    >
      <CardActionArea sx={{ justifyContent: "start" }}>
        {icon && <CardMedia align="center">{icon}</CardMedia>}
        <CardContent align="center">
          <Typography gutterBottom variant="h6" component="div">
            {title}
          </Typography>
          <Typography
            variant="body2"
            sx={{ wordWrap: "anywhere" }}
            color="text.secondary"
          >
            {des}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};

export default SimpleCard;
