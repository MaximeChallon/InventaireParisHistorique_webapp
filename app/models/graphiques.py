import altair as alt
import pandas as pd

class classe_graphiques():
	def generate_temporels_line(
		data: pd.DataFrame,
    	x_title: str,
    	padding: int = 5,
    	width: int = 700,
    	height: int = 500
		):
		return (
			alt.Chart(data)
    		.mark_line(point={"size": 70}, color='red')
    		.encode(
            	x=alt.X("Date_inventaire", title=x_title),
            	y=alt.Y(f"occurences", title="Nombre de photos inventoriées"),
            	tooltip=[
                	alt.Tooltip(f"occurences", title="Nombre de photos inventoriées"),
                	alt.Tooltip("Date_inventaire", title=x_title, type="temporal"),
            	],
        	)
        	.configure_scale(continuousPadding=padding)
        	.properties(width=width, height=height)
        	.interactive()
            )

	def generate_temporels_bar(
		data: pd.DataFrame,
        x_title: str,
        padding: int = 5,
        width: int = 700,
        height: int = 500):
		return (
            alt.Chart(data)
            .mark_bar(color='red')
            .encode(
                x=alt.X("Date_inventaire", title=x_title),
                y=alt.Y(f"occurences", title="Nombre de photos inventoriées"),
                tooltip=[
                alt.Tooltip(f"occurences", title="Nombre de photos inventoriées"),
                alt.Tooltip("Date_inventaire", title=x_title, type="temporal")
                ],
                )
            .configure_scale(continuousPadding=padding)
            .properties(width=width, height=height)
            .interactive()
            )