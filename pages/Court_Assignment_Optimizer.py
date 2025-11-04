import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime
import math

st.set_page_config(page_title="Court Assignment Optimizer", page_icon="🎾")

st.title("🎾 Court Assignment Optimizer")
st.markdown("""
This tool helps you optimally distribute players across courts based on their rankings.
Upload an Excel file with player names and rankings, and get balanced court assignments.
""")

class CourtAssignmentOptimizer:
    def __init__(self):
        self.players_data = None
        self.players_data_filtered = None
        self.court_assignments = {}
        self.min_players_per_court = 6
        self.max_players_per_court = 8
        self.min_courts_available = 1
        self.higher_is_better = False  # Always use 1=best, higher=worse system
    
    def load_players_from_csv(self, uploaded_file):
        """Load players data from CSV file"""
        try:
            # Try to read the CSV file
            df = pd.read_csv(uploaded_file)
            
            # Validate the required columns
            if len(df.columns) < 2:
                st.error("CSV file must have at least 2 columns: Player Name and Ranking")
                return False
            
            # Assume first column is player name, second is ranking
            df.columns = ['Player_Name', 'Ranking'] + list(df.columns[2:])
            
            # Remove any rows with missing player names
            df = df.dropna(subset=['Player_Name'])
            
            # If ranking is missing, assign a default ranking
            df['Ranking'] = pd.to_numeric(df['Ranking'], errors='coerce')
            df['Ranking'] = df['Ranking'].fillna(df['Ranking'].mean() if not df['Ranking'].isna().all() else 5.0)
            
            self.players_data = df[['Player_Name', 'Ranking']].copy()
            return True
            
        except Exception as e:
            st.error(f"Error reading CSV file: {str(e)}")
            return False
    
    def optimize_court_assignments(self):
        """Optimize player distribution across courts using sequential filling"""
        # Use filtered data if available, otherwise use all data
        data_to_use = self.players_data_filtered if self.players_data_filtered is not None else self.players_data
        
        if data_to_use is None or len(data_to_use) == 0:
            return False
        
        # Sort players by ranking (best players first - 1, 2, 3... where 1 is best)
        sorted_players = data_to_use.sort_values('Ranking', ascending=True).reset_index(drop=True)
        
        # Sequential filling: fill courts with top players first
        config = self._distribute_players_sequentially(sorted_players)
        
        if config:
            self.court_assignments = config
            return True
        
        return False
    
    def _distribute_players_sequentially(self, sorted_players):
        """Distribute players sequentially - fill courts with optimal number based on total players"""
        total_players = len(sorted_players)
        
        # Calculate the minimum number of courts needed to fit all players
        min_courts_needed = math.ceil(total_players / self.max_players_per_court)
        max_courts_possible = total_players // self.min_players_per_court
        
        # Use the minimum courts needed (ignore user's minimum courts setting for optimal distribution)
        optimal_courts = min_courts_needed
        
        # But ensure we don't exceed what's physically possible with minimum players
        if optimal_courts > max_courts_possible:
            optimal_courts = max_courts_possible
        
        # Show information about court optimization
        if self.min_courts_available > optimal_courts:
            st.info(f"📋 Using {optimal_courts} courts instead of {self.min_courts_available} for optimal player distribution")
        
        courts = [[] for _ in range(optimal_courts)]
        
        # Calculate base players per court and extra players
        base_players_per_court = total_players // optimal_courts
        extra_players = total_players % optimal_courts
        
        # Distribute players sequentially
        player_idx = 0
        
        for court_idx in range(optimal_courts):
            # Each court gets base players + 1 extra if there are extras left
            # Extra players go to HIGHER courts first (courts with worse players)
            extra_for_this_court = 1 if (optimal_courts - 1 - court_idx) < extra_players else 0
            players_for_this_court = base_players_per_court + extra_for_this_court
            
            # Add players to this court
            for _ in range(players_for_this_court):
                if player_idx < len(sorted_players):
                    player = sorted_players.iloc[player_idx]
                    courts[court_idx].append({
                        'name': player['Player_Name'],
                        'ranking': player['Ranking']
                    })
                    player_idx += 1
        
        return courts

    def _rebalance_courts(self, courts):
        """Rebalance courts to meet size requirements"""
        # Simple rebalancing: move players from oversized courts to undersized ones
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            oversized_courts = [i for i, court in enumerate(courts) if len(court) > self.max_players_per_court]
            undersized_courts = [i for i, court in enumerate(courts) if len(court) < self.min_players_per_court]
            
            if not oversized_courts or not undersized_courts:
                break
            
            # Move a player from oversized to undersized court
            from_court = oversized_courts[0]
            to_court = undersized_courts[0]
            
            # Move the lowest ranked player from oversized court
            player_to_move = min(courts[from_court], key=lambda p: p['ranking'])
            courts[from_court].remove(player_to_move)
            courts[to_court].append(player_to_move)
            
            iteration += 1
        
        return courts
    
    def get_assignment_summary(self):
        """Get summary statistics of the court assignments"""
        if not self.court_assignments:
            return None
        
        summary = {
            'total_courts': len(self.court_assignments),
            'total_players': sum(len(court) for court in self.court_assignments),
            'players_per_court': [len(court) for court in self.court_assignments],
            'avg_ranking_per_court': []
        }
        
        for court in self.court_assignments:
            if len(court) > 0:
                avg_ranking = sum(p['ranking'] for p in court) / len(court)
                summary['avg_ranking_per_court'].append(round(avg_ranking, 2))
            else:
                summary['avg_ranking_per_court'].append(0)
        
        return summary

# Initialize the optimizer
if 'optimizer' not in st.session_state:
    st.session_state.optimizer = CourtAssignmentOptimizer()

# File upload section
st.header("📁 Upload Player Data")
uploaded_file = st.file_uploader(
    "Choose a CSV file with player names and rankings",
    type=['csv'],
    help="CSV file should have two columns: Player Name and Ranking (numeric values)"
)

if uploaded_file is not None:
    if st.session_state.optimizer.load_players_from_csv(uploaded_file):
        st.success(f"✅ Successfully loaded {len(st.session_state.optimizer.players_data)} players")
        
        # Display the loaded data
        st.subheader("📊 Loaded Player Data")
        st.dataframe(st.session_state.optimizer.players_data, use_container_width=True)
        
        # Player Information
        st.header("🔍 Player Information")
        
        # Show current top players (always 1=best, higher=worse)
        top_players = st.session_state.optimizer.players_data.nsmallest(5, 'Ranking')
        st.caption("🏆 Top 5 players (lowest rankings = best players):")
        
        for idx, (_, player) in enumerate(top_players.iterrows(), 1):
            st.text(f"{idx}. {player['Player_Name']} (Ranking: {player['Ranking']})")
        
        # Use all players (no filtering)
        filtered_players = st.session_state.optimizer.players_data.copy()
        
        # Update the optimizer with all data (always use 1=best system)
        st.session_state.optimizer.players_data_filtered = filtered_players
        st.session_state.optimizer.higher_is_better = False  # Always use 1=best system
        
        # Court configuration
        st.header("⚙️ Court Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            min_players = st.number_input(
                "Minimum players per court",
                min_value=4,
                max_value=10,
                value=6,
                help="Minimum number of players that must be assigned to each court"
            )
        
        with col2:
            max_players = st.number_input(
                "Maximum players per court",
                min_value=min_players,
                max_value=12,
                value=8,
                help="Maximum number of players that can be assigned to each court"
            )
        
        with col3:
            min_courts = st.number_input(
                "Minimum courts available",
                min_value=1,
                max_value=20,
                value=1,
                help="Minimum number of courts you have available for play"
            )
        
        st.session_state.optimizer.min_players_per_court = min_players
        st.session_state.optimizer.max_players_per_court = max_players
        st.session_state.optimizer.min_courts_available = min_courts
        
        # Optimize button
        if st.button("🎯 Optimize Court Assignments", type="primary", use_container_width=True):
            with st.spinner("Optimizing court assignments..."):
                if st.session_state.optimizer.optimize_court_assignments():
                    st.success("✅ Court assignments optimized successfully!")
                else:
                    st.error("❌ Could not create valid court assignments with the given constraints.")

# Display results if assignments exist
if st.session_state.optimizer.court_assignments:
    st.header("🏆 Optimized Court Assignments")
    
    # Summary statistics
    summary = st.session_state.optimizer.get_assignment_summary()
    if summary:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Courts", summary['total_courts'])
        with col2:
            st.metric("Total Players", summary['total_players'])
        with col3:
            avg_players = summary['total_players'] / summary['total_courts']
            st.metric("Avg Players/Court", f"{avg_players:.1f}")
        with col4:
            filled_courts = sum(1 for court in st.session_state.optimizer.court_assignments if len(court) >= st.session_state.optimizer.min_players_per_court)
            st.metric("Filled Courts", f"{filled_courts}/{summary['total_courts']}")
        
        # Detailed court assignments
        for i, court in enumerate(st.session_state.optimizer.court_assignments, 1):
            # Determine court status
            court_status = ""
            if len(court) >= st.session_state.optimizer.min_players_per_court:
                if len(court) == st.session_state.optimizer.max_players_per_court:
                    court_status = " ✅ (Full)"
                else:
                    court_status = " ✅ (Active)"
            else:
                court_status = " ⏳ (Filling)"
            
            with st.expander(f"🎾 Court {i}{court_status} - {len(court)} players (Avg Ranking: {summary['avg_ranking_per_court'][i-1]})", expanded=True):
                court_df = pd.DataFrame(court)
                # Sort players within court by ranking (1=best, 2=next best, etc.)
                court_df = court_df.sort_values('ranking', ascending=True).reset_index(drop=True)
                court_df.index = court_df.index + 1
                
                # Add position information
                court_df['Position'] = [f"#{j}" for j in range(1, len(court_df) + 1)]
                court_df = court_df[['Position', 'name', 'ranking']]
                
                st.dataframe(court_df, use_container_width=True)
        
        # Export section
        st.header("💾 Export Court Assignments")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export as summary CSV
            summary_data = []
            for i, court in enumerate(st.session_state.optimizer.court_assignments, 1):
                for player in court:
                    summary_data.append({
                        'Court': f'Court {i}',
                        'Player_Name': player['name'],
                        'Ranking': player['ranking']
                    })
            
            summary_df = pd.DataFrame(summary_data)
            csv_summary = summary_df.to_csv(index=False)
            
            st.download_button(
                label="📊 Download Summary CSV",
                data=csv_summary,
                file_name=f'court_assignments_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )
        
        with col2:
            # Export individual court CSV files
            if st.button("📁 Generate Individual Court Files", use_container_width=True):
                st.success("Individual court files generated! Use the download buttons below.")
        
        # Individual court file downloads
        if len(st.session_state.optimizer.court_assignments) > 0:
            st.subheader("📄 Individual Court Files")
            
            for i, court in enumerate(st.session_state.optimizer.court_assignments, 1):
                # Create CSV in the format expected by the existing system
                court_data = {
                    f'Court #{i}': [f'Court #{i}'] + [p['name'] for p in court],
                    'Game 1': ['Game 1'] + ['1'] * len(court)
                }
                
                # Add more game columns for variety (this is a simplified version)
                for game_num in range(2, 11):
                    court_data[f'Game {game_num}'] = [f'Game {game_num}'] + [''] * len(court)
                
                court_df = pd.DataFrame.from_dict(court_data, orient='index').T
                court_csv = court_df.to_csv(index=False, header=False)
                
                st.download_button(
                    label=f"📄 Download Court {i} CSV",
                    data=court_csv,
                    file_name=f'court_{i}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv',
                    key=f'court_{i}_download'
                )

# Instructions section
st.sidebar.header("📋 Instructions")
st.sidebar.markdown("""
### How to use:

1. **Prepare your CSV file** with two columns:
   - Column 1: Player names
   - Column 2: Rankings (numeric values)

2. **Upload the file** using the file uploader

3. **Configure court settings**:
   - Min/max players per court
   - Minimum courts available

4. **Click "Optimize"** to generate court assignments

5. **Download** the results as CSV files

### Ranking System:

**� Fixed Ranking System:**
- **1 = Best player, higher numbers = worse players**
- **Example**: Ranking 1.5 beats ranking 2.0 beats ranking 10.0
- **Range**: Typically 1-100 (1 being the top player)

### Distribution Method:

**📈 Sequential Filling:**
- Fills courts with top players first
- Uses minimum number of courts needed for all players
- Court 1 gets best players, Court 2 gets next best, etc.
- Extra players are distributed to earlier courts first

### Features:
- � Fixed ranking system (1=best)
- 📈 Optimal sequential court filling
- 🏟️ Smart court count optimization
- 📊 Detailed assignment statistics
- 💾 Multiple export formats
- 🎾 Compatible with existing Loboton system
""")

# Example data section
st.sidebar.header("📝 Example Data Format")
example_data = pd.DataFrame({
    'Player Name': ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve', 'Frank'],
    'Ranking': [9.5, 8.2, 7.8, 6.5, 5.9, 4.3]
})

st.sidebar.dataframe(example_data, use_container_width=True)

# Download example template
example_csv = example_data.to_csv(index=False)
st.sidebar.download_button(
    label="📥 Download Example Template",
    data=example_csv,
    file_name='player_ranking_template.csv',
    mime='text/csv'
)