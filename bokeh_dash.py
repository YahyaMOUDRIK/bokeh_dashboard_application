import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select, HoverTool
from bokeh.layouts import row, column

quantity_producted_df = pd.read_excel('quantity_producted.xlsx')
surface_df = pd.read_excel('surface_cultivee.xlsx') 

# Changer occurance en une date
quantity_producted_df['Occurrence'] = pd.to_datetime(quantity_producted_df['Occurrence'].apply(lambda x: x.split('/')[0]), format='%Y')
surface_df['Occurrence'] = pd.to_datetime(surface_df['Occurrence'].apply(lambda x: x.split('/')[0]), format='%Y')

# Créer une liste de tous les produits
products = quantity_producted_df['Produit'].unique().tolist()

# Create initial ColumnDataSource for production data
initial_product = products[0]
initial_production = quantity_producted_df[quantity_producted_df['Produit'] == initial_product]
source_production = ColumnDataSource(data={
    'Occurrence': initial_production['Occurrence'],
    'Valeur': initial_production['Valeur']
})

# Create initial ColumnDataSource for surface data
initial_surface = surface_df[surface_df['Produit'] == initial_product]
source_surface = ColumnDataSource(data={
    'Occurrence': initial_surface['Occurrence'],
    'Valeur': initial_surface['Valeur']
})

# Create a select widget for choosing the product
product_select = Select(title='Sélectionner un produit:', value=initial_product, options=products)

# Create the production plot
plot_production = figure(x_axis_type='datetime', height=400, width=800, title='Évolution de la production')
plot_production.line(x='Occurrence', y='Valeur', source=source_production, line_width=2)
plot_production.xaxis.axis_label = 'Année'
plot_production.yaxis.axis_label = 'Production'

# Create the surface plot
plot_surface = figure(x_axis_type='datetime', height=400, width=800, title='Évolution de la surface cultivée')
plot_surface.line(x='Occurrence', y='Valeur', source=source_surface, line_width=2)
plot_surface.xaxis.axis_label = 'Année'
plot_surface.yaxis.axis_label = 'Surface cultivée'

# Add hover tool
hover_tool_production = HoverTool(tooltips=[('Année', '@Occurrence{%F}'), ('Production', '@Valeur')], formatters={'@Occurrence': 'datetime'})
hover_tool_surface = HoverTool(tooltips=[('Année', '@Occurrence{%F}'), ('Surface', '@Valeur')], formatters={'@Occurrence': 'datetime'})
plot_production.add_tools(hover_tool_production)
plot_surface.add_tools(hover_tool_surface)

# Update the data sources based on the selected product
def update_data(attr, old, new):
    selected_product = product_select.value
    filtered_production = quantity_producted_df[quantity_producted_df['Produit'] == selected_product]
    filtered_surface = surface_df[surface_df['Produit'] == selected_product]
    source_production.data = {
        'Occurrence': filtered_production['Occurrence'],
        'Valeur': filtered_production['Valeur']
    }
    source_surface.data = {
        'Occurrence': filtered_surface['Occurrence'],
        'Valeur': filtered_surface['Valeur']
    }

# Add callback to the select widget
product_select.on_change('value', update_data)

# Create the other visualizations
production_annuelle = quantity_producted_df.groupby('Occurrence')['Valeur'].sum().reset_index()
plot_production_annuelle = figure(x_axis_type='datetime', height=400, width=800, title='Production avec le temps')
plot_production_annuelle.line(x='Occurrence', y='Valeur', source=ColumnDataSource(production_annuelle), line_width=2)
plot_production_annuelle.xaxis.axis_label = 'Année'
plot_production_annuelle.yaxis.axis_label = 'Production'

surface_cultivée = surface_df.groupby('Occurrence')['Valeur'].sum().reset_index()
plot_surface_cultivée = figure(x_axis_type='datetime', height=400, width=800, title='Surface cultivée par an')
plot_surface_cultivée.line(x='Occurrence', y='Valeur', source=ColumnDataSource(surface_cultivée), line_width=2)
plot_surface_cultivée.xaxis.axis_label = 'Année'
plot_surface_cultivée.yaxis.axis_label = 'Surface'

# Add the other visualizations to the layout
layout = column(
    product_select,
    row(plot_production, plot_surface),
    row(plot_production_annuelle, plot_surface_cultivée)
)

# Create the Bokeh app
curdoc().add_root(layout)

