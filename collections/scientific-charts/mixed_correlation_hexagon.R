# Advanced Mixed Correlation Matrix with TRUE HEXAGONS
# Using geom_polygon for custom hexagon shapes in upper triangle

library(tidyverse)
library(ggplot2)
library(reshape2)

set.seed(42)

# ============================================================================
# 1. Generate data
# ============================================================================
n <- 100
n_vars <- 12

data <- matrix(rnorm(n * n_vars), ncol = n_vars)
for (i in 2:n_vars) {
  data[, i] <- data[, i] + 0.5 * data[, i-1]
}
data[, 5] <- data[, 5] - 0.6 * data[, 2]
data[, 8] <- data[, 8] - 0.4 * data[, 3]

colnames(data) <- paste0("Var", 1:n_vars)
df <- as.data.frame(data)

# ============================================================================
# 2. Calculate correlations and p-values
# ============================================================================
cor_matrix <- cor(df)
p_matrix <- matrix(NA, nrow = n_vars, ncol = n_vars)

for (i in 1:n_vars) {
  for (j in 1:n_vars) {
    if (i != j) {
      test <- cor.test(df[, i], df[, j])
      p_matrix[i, j] <- test$p.value
    } else {
      p_matrix[i, j] <- 0
    }
  }
}

get_significance <- function(p) {
  case_when(
    p < 0.001 ~ "***",
    p < 0.01 ~ "**",
    p < 0.05 ~ "*",
    TRUE ~ ""
  )
}

# ============================================================================
# 3. Create hexagon coordinates function
# ============================================================================
create_hexagon <- function(x, y, size = 0.4) {
  angles <- seq(0, 2*pi, length.out = 7)
  data.frame(
    x = x + size * cos(angles),
    y = y + size * sin(angles)
  )
}

# ============================================================================
# 4. Prepare plot data
# ============================================================================
cor_long <- melt(cor_matrix)
colnames(cor_long) <- c("Var1", "Var2", "correlation")

p_long <- melt(p_matrix)
colnames(p_long) <- c("Var1", "Var2", "p_value")

plot_data <- cor_long %>%
  left_join(p_long, by = c("Var1", "Var2")) %>%
  mutate(
    significance = get_significance(p_value),
    abs_cor = abs(correlation),
    x = as.numeric(Var2),
    y = as.numeric(Var1),
    position = case_when(
      Var1 == Var2 ~ "diagonal",
      as.numeric(Var1) > as.numeric(Var2) ~ "lower",
      TRUE ~ "upper"
    ),
    label = ifelse(position == "lower" | position == "diagonal",
                   paste0(sprintf("%.2f", correlation), "\n", significance),
                   "")
  )

# ============================================================================
# 5. Create hexagon data for upper triangle
# ============================================================================
hexagon_data <- plot_data %>%
  filter(position == "upper") %>%
  rowwise() %>%
  mutate(
    # Scale hexagon size by correlation strength
    hex_size = 0.35 * abs_cor + 0.1
  ) %>%
  group_by(Var1, Var2) %>%
  do({
    hex_coords <- create_hexagon(.$x, .$y, size = .$hex_size)
    hex_coords$correlation <- .$correlation
    hex_coords$Var1 <- .$Var1
    hex_coords$Var2 <- .$Var2
    hex_coords
  }) %>%
  ungroup()

# ============================================================================
# 6. Create the plot
# ============================================================================
p <- ggplot() +

  # Lower triangle: Heatmap tiles
  geom_tile(data = filter(plot_data, position %in% c("lower", "diagonal")),
            aes(x = x, y = y, fill = correlation),
            color = "white", size = 1) +

  # Lower triangle: Text labels
  geom_text(data = filter(plot_data, position %in% c("lower", "diagonal")),
            aes(x = x, y = y, label = label,
                color = ifelse(abs(correlation) > 0.5, "white", "black")),
            size = 3.5, fontface = "bold", lineheight = 0.8) +

  # Upper triangle: Hexagons
  geom_polygon(data = hexagon_data,
               aes(x = x, y = y,
                   group = interaction(Var1, Var2),
                   fill = correlation),
               color = "white", size = 1) +

  # Color scale
  scale_fill_gradient2(
    low = "#d73027",
    mid = "#ffffbf",
    high = "#4575b4",
    midpoint = 0,
    limits = c(-1, 1),
    name = "Correlation\nCoefficient"
  ) +

  scale_color_identity() +

  # Axis labels
  scale_x_continuous(
    breaks = 1:n_vars,
    labels = paste0("Var", 1:n_vars),
    expand = c(0.02, 0.02)
  ) +
  scale_y_continuous(
    breaks = 1:n_vars,
    labels = paste0("Var", 1:n_vars),
    expand = c(0.02, 0.02)
  ) +

  # Labels and title
  labs(
    title = "Mixed Correlation Matrix with Hexagons",
    subtitle = "Lower: Heatmap with significance stars | Upper: Hexagons sized by |correlation|",
    x = NULL,
    y = NULL
  ) +

  # Theme
  theme_minimal() +
  theme(
    panel.grid = element_blank(),
    panel.background = element_rect(fill = "white", color = NA),
    plot.background = element_rect(fill = "white", color = NA),

    axis.text.x = element_text(angle = 45, hjust = 1, size = 11, face = "bold"),
    axis.text.y = element_text(size = 11, face = "bold"),

    plot.title = element_text(size = 16, face = "bold", hjust = 0.5),
    plot.subtitle = element_text(size = 10, hjust = 0.5, color = "gray40",
                                  margin = margin(b = 15)),

    legend.position = "right",
    legend.title = element_text(size = 11, face = "bold"),
    legend.text = element_text(size = 10),
    legend.key.height = unit(1.5, "cm"),

    aspect.ratio = 1,
    plot.margin = margin(10, 10, 10, 10)
  ) +

  coord_fixed()

print(p)

# Save
ggsave("mixed_correlation_hexagon.png",
       plot = p,
       width = 14,
       height = 12,
       dpi = 300,
       bg = "white")

cat("Hexagon plot saved as 'mixed_correlation_hexagon.png'\n")

# ============================================================================
# 7. Summary statistics
# ============================================================================
cat("\n=== Correlation Analysis Summary ===\n")
cat("Variables:", n_vars, "\n")
cat("Observations:", n, "\n")
cat("Correlation range:",
    sprintf("[%.3f, %.3f]",
            min(cor_matrix[cor_matrix != 1]),
            max(cor_matrix[cor_matrix != 1])), "\n")
cat("Mean |correlation|:",
    sprintf("%.3f", mean(abs(cor_matrix[upper.tri(cor_matrix)]))), "\n")
cat("Significant pairs (p<0.05):",
    sum(p_matrix[upper.tri(p_matrix)] < 0.05, na.rm = TRUE),
    "/", sum(upper.tri(p_matrix)), "\n")
