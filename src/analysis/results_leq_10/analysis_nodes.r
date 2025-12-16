library(tidyverse)
library(ggplot2)

df1 <- read_csv("all_graphs_9n.csv") %>%
  mutate(type = "splosni")

df1_10 <- read_csv("gpn_values_n10.csv") %>%
  mutate(type = "splosni",
         num_nodes = 10)

df2 <- read_csv("gpn_class_data.csv") %>%
  mutate(id = name) %>%
  select(1, 3, 5, 6)
  
df1_vsi <- bind_rows(df1, df1_10)

all_df <- bind_rows(df1_vsi, df2)
total_graphs <- nrow(all_df)


# GRAF ZA VOZLIŠČA
graph_nodes <- all_df %>%
  group_by(type, num_nodes) %>%
  summarise(
    mean_gpn = mean(gpn_num),
    max_gpn = max(gpn_num),
    min_gpn = min(gpn_num),
    count = n(),
    .groups = 'drop'
  ) %>%
  arrange(type, num_nodes)

p_nodes_simple <- ggplot(graph_nodes, aes(x = num_nodes)) +
  
  # OBMOČJA
  geom_ribbon(
    data = graph_nodes %>% filter(type == "splosni"),
    aes(ymin = min_gpn, ymax = max_gpn, fill = "Splošni"),
    alpha = 0.2
  ) +
  geom_ribbon(
    data = graph_nodes %>% filter(type == "bipartite"),
    aes(ymin = min_gpn, ymax = max_gpn, fill = "Dvodelni"),
    alpha = 0.2
  ) +
  geom_ribbon(
    data = graph_nodes %>% filter(type == "triangle-free"),
    aes(ymin = min_gpn, ymax = max_gpn, fill = "Brez trikotnikov"),
    alpha = 0.2
  ) +
  geom_ribbon(
    data = graph_nodes %>% filter(type == "cubic"),
    aes(ymin = min_gpn, ymax = max_gpn, fill = "Kubični"),
    alpha = 0.2
  ) +
  
  # POVPREČJA
  geom_line(
    data = graph_nodes %>% filter(type == "splosni"),
    aes(y = mean_gpn, color = "Splošni"),
    size = 1.2
  ) +
  geom_point(
    data = graph_nodes %>% filter(type == "splosni"),
    aes(y = mean_gpn, color = "Splošni"),
    size = 3
  ) +
  
  geom_line(
    data = graph_nodes %>% filter(type == "bipartite"),
    aes(y = mean_gpn, color = "Dvodelni"),
    size = 1.2
  ) +
  geom_point(
    data = graph_nodes %>% filter(type == "bipartite"),
    aes(y = mean_gpn, color = "Dvodelni"),
    size = 3
  ) +
  
  geom_line(
    data = graph_nodes %>% filter(type == "triangle-free"),
    aes(y = mean_gpn, color = "Brez trikotnikov"),
    size = 1.2
  ) +
  geom_point(
    data = graph_nodes %>% filter(type == "triangle-free"),
    aes(y = mean_gpn, color = "Brez trikotnikov"),
    size = 3
  ) +
  
  geom_line(
    data = graph_nodes %>% filter(type == "cubic"),
    aes(y = mean_gpn, color = "Kubični"),
    size = 1.2
  ) +
  geom_point(
    data = graph_nodes %>% filter(type == "cubic"),
    aes(y = mean_gpn, color = "Kubični"),
    size = 3
  ) +
  
  # BARVE
  scale_color_manual(
    name = "Povprečje",
    values = c(
      "Splošni" = "#1f77b4",
      "Dvodelni" = "#ff7f0e",
      "Brez trikotnikov" = "#d62728",
      "Kubični" = "#2ca02c"
    ),
    guide = guide_legend(order = 1)
  ) +
  
  scale_fill_manual(
    name = "Razpon (min-max)",
    values = c(
      "Splošni" = "#1f77b4",
      "Dvodelni" = "#ff7f0e",
      "Brez trikotnikov" = "#d62728",
      "Kubični" = "#2ca02c"
    ),
    guide = guide_legend(order = 2)
  ) +
  
  labs(
    title = "Število geodetskih podpoti (gpn) glede na število vozlišč",
    subtitle = "Prikaz povprečij in razponov za vse štiri tipe grafov",
    x = "Število vozlišč",
    y = "Število geodetskih podpoti (gpn)",
    caption = paste("Skupaj analiziranih grafov:", total_graphs)
  ) +
  
  theme_minimal(base_size = 12) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold", size = 14),
    plot.subtitle = element_text(hjust = 0.5, size = 12),
    plot.caption = element_text(hjust = 1, face = "italic", size = 10),
    legend.position = "bottom",
    legend.box = "horizontal",
    legend.spacing.x = unit(0.5, "cm"),
    legend.text = element_text(size = 10),
    legend.title = element_text(size = 11, face = "bold"),
    panel.grid.minor = element_blank()
  ) +
  
  scale_x_continuous(breaks = unique(graph_nodes$num_nodes)) +
  scale_y_continuous(breaks = scales::pretty_breaks(n = 12))

# 5. PRIKAŽI GRAF
print(p_nodes_simple)

# 6. SHARNI KOT JPG
ggsave("gpn_vs_vozlisca_10.jpg", p_nodes_simple, 
       width = 13, height = 8, dpi = 300, bg = "white")


##TABELA Z OPT GRAFI
df2_tabela <- read_csv("gpn_class_data.csv") %>%
  group_by(num_nodes) %>%
  filter(gpn_num == max(gpn_num)) %>%
  ungroup() %>%
  select(st_vozlisc = num_nodes, unikatno_ime = name, st_povezav = num_edges, st_gpn = gpn_num)

rezultat <- df2_tabela %>%
  group_by(st_vozlisc) %>%
  slice(1) %>%
  ungroup()

# Razvrstimo po številu vozlišč
rezultat <- rezultat %>%
  arrange(st_vozlisc)

# Prikaz rezultata
print(rezultat)