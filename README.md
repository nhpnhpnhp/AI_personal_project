# AI_personal_project
1. Mục tiêu
Mục tiêu của chương trình là xây dựng một hệ thống giải bài toán 8-Puzzle bằng cách áp dụng nhiều nhóm thuật toán khác nhau trong lĩnh vực Trí Tuệ Nhân Tạo. Việc này nhằm so sánh hiệu quả giữa các thuật toán, hiểu rõ đặc điểm, ưu nhược điểm của từng phương pháp trong việc giải quyết bài toán tìm kiếm, từ đó nâng cao khả năng chọn lựa giải pháp phù hợp cho các vấn đề tương tự trong thực tế.

2. Nội dung
Chương trình được tổ chức thành nhiều nhóm thuật toán dựa theo phân loại trong AI:

  1.Uniformed Search: BFS, DFS, UCS, IDDFS

  2.Informed Search: Greedy, A*, IDA*, Genetic Algorithm (GA), Beam Search

  3.Local Search: Simple Hill Climbing, Steepest Hill Climbing, Stochastic Hill Climbing, Simulated Annealing (SA)

  4.Complex Environments: Nondeterministic search, No observation search, Partially observable search

  5.Constraint Satisfaction Problems (CSPs): Backtracking, Min-conflict, Backtracking with Forward Checking

  6.Reinforcement Learning: Q-Learning

2.1. Các thuật toán tìm kiếm có thông tin (Informed Search)

IDA* – Iterative Deepening A*
![IDA](https://github.com/user-attachments/assets/f540281c-17c7-4aa0-bf0d-f1182f02ff3c)

Thuật toán IDA* kết hợp hai chiến lược mạnh mẽ:

A*: Tìm kiếm theo chi phí tổng f(n) = g(n) + h(n) (chi phí đến hiện tại + ước lượng đến đích).

Iterative Deepening (tìm kiếm sâu dần): Tìm theo mức giới hạn chi phí và mở rộng dần mức giới hạn này.

IDA* tận dụng bộ nhớ thấp của DFS và sức mạnh định hướng của heuristic trong A*. Đây là một trong những thuật toán hiệu quả nhất cho các bài toán như 8-Puzzle hoặc 15-Puzzle.

    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State): Ma trận 3x3 gồm các ô số từ 1 đến 8 và một ô trống (0). Đảm bảo trạng thái có lời giải.

    Tập hành động (Actions): Di chuyển ô trống theo các hướng trái, phải, lên, xuống.

    Hàm chuyển trạng thái (Transition Model): Hoán đổi vị trí ô trống với ô lân cận theo hướng hành động.

    Kiểm tra mục tiêu (Goal Test): So sánh trạng thái hiện tại với trạng thái đích (ví dụ: 1–2–3 | 4–5–6 | 7–8–0).

    Hàm chi phí (Path Cost): Mỗi bước di chuyển có chi phí 1. Tổng chi phí = tổng số bước.

    Heuristic (Hàm ước lượng h(n)): Dùng để định hướng tìm kiếm. Phổ biến:

    Số ô sai vị trí (Misplaced Tiles).

    Tổng khoảng cách Manhattan (Manhattan Distance) – thường hiệu quả hơn.

    Hoạt động của thuật toán IDA*
    Khởi tạo threshold bằng giá trị f(start) = g(start) + h(start) của trạng thái ban đầu.

    Thực hiện DFS với giới hạn chi phí không vượt quá threshold.

    Nếu tìm thấy đích → trả về lời giải.

    Nếu không, tăng threshold lên giá trị nhỏ nhất của f(n) đã vượt giới hạn trong lần tìm trước và lặp lại.

    Quá trình tiếp tục cho đến khi tìm được lời giải hoặc không còn trạng thái nào để mở rộng.

    IDA* sử dụng DFS có giới hạn chi phí, không phải giới hạn độ sâu.

    Solution:
    Trả về chuỗi hành động từ trạng thái ban đầu đến trạng thái đích, được định hướng bởi hàm f(n) = g(n) + h(n).

    Đảm bảo lời giải tối ưu nếu heuristic thỏa mãn tính nhất quán (consistent).
    
    Hiệu suất
    Ưu điểm:
    Tối ưu hóa bộ nhớ: chỉ cần dùng không gian giống DFS.
    
    Tìm lời giải tối ưu nếu heuristic phù hợp.
    
    Thích hợp cho bài toán có không gian trạng thái lớn như 15-Puzzle.
    
    Nhược điểm:
    Phải duyệt lại nhiều trạng thái trong mỗi vòng lặp do đặc trưng của DFS.
    
    Hiệu suất phụ thuộc lớn vào chất lượng của heuristic.
    
    Không hiệu quả nếu heuristic kém hoặc không nhất quán.

  Beam Search
    ![beam](https://github.com/user-attachments/assets/9e31a041-df47-4501-890e-de4192f9d398)

  Thuật toán Beam Search là phiên bản giới hạn bộ nhớ của tìm kiếm theo Best-First Search. Tại mỗi bước mở rộng, chỉ giữ lại k nút có giá trị đánh giá tốt nhất (gọi là beam width) thay vì giữ toàn bộ các nút sinh ra. Điều này giúp giảm bộ nhớ và tập trung vào các nhánh hứa hẹn nhất.

    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State):
    Ma trận 3x3 gồm các ô số 1–8 và một ô trống (0). Đảm bảo trạng thái có lời giải.
    
    Tập hành động (Actions):
    Di chuyển ô trống theo bốn hướng: trái, phải, lên, xuống.
    
    Hàm chuyển trạng thái (Transition Model):
    Hoán đổi vị trí ô trống với ô kề.
    
    Kiểm tra mục tiêu (Goal Test):
    So sánh trạng thái hiện tại với trạng thái đích.
    
    Hàm chi phí / Hàm đánh giá:
    Trong Beam Search, ta thường chỉ dựa vào heuristic h(n) để chọn nút tốt, bỏ qua chi phí g(n).
    
    Hoạt động của thuật toán Beam Search
    Khởi tạo
    Tạo danh sách beam (beam list) gồm trạng thái ban đầu.
    
    Lặp lại
    • Với mỗi nút trong beam hiện tại: mở rộng các trạng thái con.
    • Gom tất cả trạng thái con vào một danh sách tạm.
    • Chọn ra k trạng thái con có giá trị heuristic tốt nhất (nhỏ nhất nếu là hàm chi phí) để tạo beam mới.
    • Nếu trong beam mới có trạng thái đích → trả về lời giải.
    
    Kết thúc
    Thuật toán dừng khi tìm thấy đích hoặc không còn nút nào để mở rộng.
    
    Solution
    Trả về chuỗi hành động từ trạng thái ban đầu đến đích, theo một trong k nhánh hứa hẹn nhất.
    Lưu ý: Beam Search không đảm bảo tìm được lời giải tối ưu vì nó có thể loại bỏ nhánh tối ưu nếu không nằm trong beam tại một bước nào đó.
    
    Hiệu suất
    Ưu điểm:
    Tối ưu hóa bộ nhớ: chỉ lưu k nút tại mỗi bước.
    Nhanh hơn so với các thuật toán tìm kiếm toàn cục (như A*) nếu beam width đủ nhỏ.
    Thích hợp cho các bài toán lớn hoặc cần kết quả nhanh (ví dụ: xử lý ngôn ngữ tự nhiên, dịch máy).
    
    Nhược điểm:
    Không đảm bảo tìm được lời giải tối ưu.
    Phụ thuộc mạnh vào giá trị beam width – quá nhỏ có thể bỏ lỡ lời giải, quá lớn lại tăng chi phí tính toán.
    Hiệu quả phụ thuộc nhiều vào chất lượng heuristic.
    

  - Genetic Algorithm (GA): Sử dụng cơ chế chọn lọc tự nhiên (lai ghép, đột biến) để tiến hóa lời giải qua nhiều thế hệ.
  + Genetic Algorithm: không luôn tìm ra lời giải tối ưu, phụ thuộc nhiều vào cách biểu diễn cá thể và hàm fitness; tuy nhiên có thể hiệu quả trong không gian tìm kiếm lớn hoặc không xác định.
  + Trong GA, crossover (lai ghép) và mutation (đột biến) phải đảm bảo sinh ra cá thể hợp lệ.
    Nhưng trong 8-puzzle:
 → Nếu “trộn” hai bàn cờ, rất dễ tạo ra trạng thái không thể đạt được qua các bước hợp pháp (vì chỉ một số hoán đổi là hợp lệ).
 → Mutation (thay đổi ngẫu nhiên) cũng dễ tạo ra trạng thái vi phạm ràng buộc.
  → Việc thiết kế các toán tử GA phù hợp để giữ trạng thái hợp lệ rất khó và phức tạp.
![image](https://github.com/user-attachments/assets/cd810586-4cc8-4270-b6c1-aaa43961ebff)



Greedy Search
    ![Gready](https://github.com/user-attachments/assets/2edf4f5c-219b-47b3-af8f-671335c90f0a)

Thuật toán Greedy Search là một chiến lược tìm kiếm dựa hoàn toàn vào hàm heuristic h(n) để định hướng. Tại mỗi bước, chỉ mở rộng nút có giá trị heuristic nhỏ nhất (ước lượng gần đích nhất), mà bỏ qua chi phí đã đi (g(n)).

    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State):
    Ma trận 3x3 gồm các ô số 1–8 và một ô trống (0).
    
    Tập hành động (Actions):
    Di chuyển ô trống theo bốn hướng: trái, phải, lên, xuống.
    
    Hàm chuyển trạng thái (Transition Model):
    Hoán đổi vị trí ô trống với ô lân cận.
    
    Kiểm tra mục tiêu (Goal Test):
    Kiểm tra xem trạng thái hiện tại có giống trạng thái đích không.
    
    Hàm đánh giá:
    • Heuristic h(n) → ước lượng chi phí từ n đến đích.
    • Ví dụ: số ô sai vị trí, khoảng cách Manhattan.
    Lưu ý: Greedy Search chỉ dùng h(n), không dùng f(n) = g(n) + h(n).
    
    Hoạt động của thuật toán Greedy Search
    Khởi tạo
    Đặt trạng thái ban đầu vào tập open list.
    
    Lặp lại
    • Chọn nút n có h(n) nhỏ nhất trong open list.
    • Nếu n là trạng thái đích → trả về lời giải.
    • Nếu không, mở rộng n, thêm các trạng thái con vào open list.
    • Loại bỏ n khỏi open list, thêm vào closed list (nếu dùng).
    
    Kết thúc
    Dừng khi tìm thấy đích hoặc không còn nút nào để mở rộng.
    
    Solution
    Trả về một chuỗi hành động từ trạng thái ban đầu đến đích dựa trên hướng đi “ngắn nhất theo ước lượng”.
    
    Lưu ý:
    Greedy Search không đảm bảo tìm được lời giải tối ưu. Nó có thể rơi vào bẫy cục bộ hoặc vòng lặp nếu không cẩn thận.
    
    Hiệu suất
    Ưu điểm:
    Nhanh, vì chỉ tập trung mở rộng nút hứa hẹn nhất.
    Tốn ít bộ nhớ hơn A* (không cần lưu g(n)).
    
    Nhược điểm:
    Không đảm bảo tối ưu (dễ rơi vào lời giải không tốt nhất).
    Có thể mắc kẹt trong bẫy heuristic hoặc bị lặp vô hạn nếu không kiểm soát.
    Phụ thuộc mạnh vào chất lượng heuristic.

A* – A Star Search Algorithm
    ![A](https://github.com/user-attachments/assets/4fe45389-afc1-481b-b7b6-d45018ff7274)

Thuật toán A* kết hợp hai yếu tố quan trọng:

Tìm kiếm theo chi phí tối ưu: Xem xét tổng chi phí ước lượng để đến đích qua hàm
  f(n) = g(n) + h(n)
  • g(n): chi phí thực từ trạng thái ban đầu đến n
  • h(n): chi phí ước lượng từ n đến đích (heuristic)

Ưu tiên mở rộng nút tiềm năng: Luôn chọn nút có giá trị f(n) nhỏ nhất trong tập mở (open list).

    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State):
    Ma trận 3x3 gồm các ô số 1–8 và một ô trống (0). Đảm bảo trạng thái có thể giải được.
    
    Tập hành động (Actions):
    Di chuyển ô trống theo bốn hướng: trái, phải, lên, xuống.
    
    Hàm chuyển trạng thái (Transition Model):
    Hoán đổi vị trí ô trống với ô kề theo hướng di chuyển.
    
    Kiểm tra mục tiêu (Goal Test):
    So sánh trạng thái hiện tại với trạng thái đích (thường là 1–2–3 | 4–5–6 | 7–8–0).
    
    Hàm chi phí (Path Cost):
    Mỗi bước di chuyển có chi phí 1. Tổng chi phí = tổng số bước từ đầu đến trạng thái hiện tại.
    
    Heuristic (Hàm ước lượng h(n)):
    Giúp định hướng tìm kiếm. Thường dùng:
     • Số ô sai vị trí (Misplaced Tiles)
     • Khoảng cách Manhattan (Manhattan Distance) – hiệu quả hơn và phổ biến hơn.
    
    Hoạt động của thuật toán A*
    Khởi tạo
    Tập mở (open list) chứa trạng thái ban đầu.
    Tập đóng (closed list) rỗng.
    
    Lặp lại
    • Lấy nút n có f(n) nhỏ nhất từ open list.
    • Nếu n là đích → trả về lời giải.
    • Nếu không, thêm n vào closed list.
    • Mở rộng n: sinh các trạng thái kế cận.
    • Với mỗi trạng thái kế cận:
     – Nếu chưa nằm trong closed list hoặc có đường đi tốt hơn, tính f(n), thêm hoặc cập nhật vào open list.
    
    Kết thúc
    Thuật toán dừng khi tìm thấy đích hoặc không còn nút nào trong open list (→ không có lời giải).
    
    Solution
    Trả về chuỗi hành động tối ưu từ trạng thái ban đầu đến trạng thái đích, được xác định bởi đường đi có chi phí f(n) nhỏ nhất.
    
    Đảm bảo lời giải tối ưu nếu heuristic thỏa mãn:
    Admissible (không đánh giá quá thấp chi phí thực).
    Consistent (thỏa mãn bất đẳng thức tam giác).
    
    Hiệu suất
    Ưu điểm:
    Tìm được lời giải tối ưu nếu heuristic phù hợp.
    Thường mở rộng ít nút hơn so với tìm kiếm không heuristic (như Uniform Cost Search).
    Có thể dễ dàng tùy biến heuristic để tăng tốc tìm kiếm.
    
    Nhược điểm:
    Tốn bộ nhớ lớn: lưu toàn bộ open list và closed list.
    Hiệu suất phụ thuộc mạnh vào chất lượng heuristic.
    Không phù hợp cho không gian trạng thái cực lớn nếu không có heuristic tốt.

2.2 Các thuật toán tìm kiếm không có thông tin

BFS
![bfs](https://github.com/user-attachments/assets/ea3a408d-5e41-41c3-9bff-a147eb8d53ea)
  Thuật toán Breadth-First Search (BFS) là một trong những phương pháp tìm kiếm không sử dụng thông tin bổ sung về trạng thái đích. BFS hoạt động theo nguyên lý mở rộng tất cả các trạng thái ở mức hiện tại trước khi chuyển sang mức tiếp theo, đảm bảo tìm ra lời giải có số bước ít nhất. 
  
    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State) : Một mảng 3x3 gồm 8 ô số (1–8) và một ô trống (thường ký hiệu là 0). Vị trí các ô được sắp xếp ngẫu nhiên nhưng đảm bảo bài toán có lời giải.
    Tập hành động (Actions): Tại mỗi trạng thái, ô trống có thể được di chuyển theo 4 hướng: trái, phải, lên, xuống, tùy vào vị trí của nó trong lưới.
    Hàm chuyển trạng thái (Transition Model): Một hành động sẽ tạo ra một trạng thái mới bằng cách hoán đổi vị trí của ô trống với ô liền kề theo hướng di chuyển.
    Kiểm tra mục tiêu (Goal Test): Kiểm tra xem trạng thái hiện tại có giống với trạng thái mục tiêu hay không. Trạng thái mục tiêu thường là:
    Hàm chi phí (Path Cost): Mỗi hành động được gán chi phí là 1. Tổng chi phí bằng tổng số bước thực hiện từ trạng thái đầu đến trạng thái đích.
    Hoạt động của thuật toán BFS
      Sử dụng một hàng đợi (queue) để lưu các trạng thái chờ mở rộng.
      Khởi tạo bằng trạng thái ban đầu và đưa nó vào hàng đợi.
      Lặp lại:
      Lấy trạng thái đầu tiên khỏi hàng đợi.
      Nếu là trạng thái đích → trả về chuỗi hành động dẫn đến nó.
      Nếu không, tạo tất cả các trạng thái con (sau khi thực hiện các hành động hợp lệ).
      Thêm các trạng thái con chưa từng được duyệt vào hàng đợi.
      Quá trình dừng khi tìm thấy trạng thái đích hoặc không còn trạng thái nào để mở rộng.
      Thuật toán đảm bảo rằng trạng thái đích sẽ được tìm thấy với số bước ít nhất vì nó mở rộng theo từng mức.

    Solution:
    Lời giải là một chuỗi các hành động (ví dụ: ["Right", "Down", "Left", "Up"]) biến trạng thái ban đầu thành trạng thái đích. Với BFS, chuỗi này luôn là lời giải ngắn nhất (ít bước nhất).
    Hiệu suất:
    Ưu điểm
    Đảm bảo tìm lời giải ngắn nhất về số bước.
    Thực thi đơn giản, dễ kiểm chứng đúng sai.
    Hoàn tất trong không gian trạng thái hữu hạn như 8-Puzzle.
    Nhược điểm
    Tốn bộ nhớ nghiêm trọng nếu lời giải sâu.
    Không hiệu quả với các bài toán mở rộng như 15-Puzzle.
    Không tận dụng bất kỳ thông tin nào về mục tiêu (không có heuristic).
DFS
![DFS](https://github.com/user-attachments/assets/6f9d8922-9cbc-4d13-a732-1e31ba4b3455)

Thuật toán Depth-First Search (DFS) là một phương pháp tìm kiếm không sử dụng thông tin bổ sung về trạng thái đích. DFS hoạt động theo nguyên lý đi sâu vào nhánh con đầu tiên cho đến khi không thể đi tiếp (chạm nút lá hoặc gặp trạng thái đã duyệt), sau đó mới quay lui để tiếp tục nhánh kế tiếp. DFS không đảm bảo tìm ra lời giải tối ưu về số bước, nhưng có thể tiết kiệm bộ nhớ hơn so với BFS.

    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State): Một ma trận 3x3 gồm 8 ô số (1–8) và một ô trống (0). Trạng thái phải đảm bảo là khả giải (có lời giải tồn tại).

    Tập hành động (Actions): Di chuyển ô trống theo các hướng: lên, xuống, trái, phải, tùy theo vị trí hiện tại trong lưới.

    Hàm chuyển trạng thái (Transition Model): Thực hiện một hành động sẽ tạo ra một trạng thái mới bằng cách hoán đổi ô trống với ô liền kề theo hướng tương ứng.

    Kiểm tra mục tiêu (Goal Test): Kiểm tra xem trạng thái hiện tại có khớp với trạng thái đích đã cho không. Trạng thái mục tiêu thường là:

    Hàm chi phí (Path Cost): Mỗi hành động có chi phí là 1. Tổng chi phí là tổng số hành động đã thực hiện.

    Hoạt động của thuật toán DFS
    Sử dụng một ngăn xếp (stack) để lưu các trạng thái chờ mở rộng.

    Khởi tạo bằng trạng thái ban đầu và đưa nó vào ngăn xếp.

    Lặp lại:

    Lấy trạng thái ở đỉnh ngăn xếp ra.

    Nếu là trạng thái đích → trả về chuỗi hành động dẫn đến nó.

    Nếu không, tạo các trạng thái con hợp lệ.

    Thêm các trạng thái con chưa từng được duyệt vào ngăn xếp.

    Quá trình kết thúc khi tìm thấy trạng thái đích hoặc ngăn xếp trống.

    DFS ưu tiên đi sâu trước, nên có thể tìm ra lời giải nhanh ở những trường hợp đích nằm gần rễ theo một nhánh cụ thể. Tuy nhiên, do không duyệt theo mức, nên không đảm bảo tìm ra lời giải ngắn nhất.

    Solution:
    Lời giải là một chuỗi hành động như ["Right", "Right", "Down", "Left", "Down", "Left"] biến trạng thái ban đầu thành trạng thái đích.

    DFS không đảm bảo lời giải ngắn nhất.

    Hiệu suất
    Ưu điểm:
    Bộ nhớ ít hơn BFS, vì chỉ cần lưu các trạng thái theo chiều sâu (ngăn xếp).

    Có thể nhanh chóng tìm thấy lời giải nếu nó nằm ở nhánh đầu tiên.

    Dễ cài đặt.

    Nhược điểm:
    Không đảm bảo lời giải ngắn nhất.

    Có thể rơi vào vòng lặp vô hạn nếu không kiểm tra trạng thái đã duyệt.

    Không hiệu quả nếu lời giải nằm ở mức rất nông nhưng DFS lại đi lạc quá sâu ở nhánh sai.

UCS – Uniform Cost Search
![UCS](https://github.com/user-attachments/assets/534b8869-ce2b-4793-ac23-4c6deeeb8523)

  Thuật toán Uniform Cost Search (UCS) là một thuật toán tìm kiếm không có thông tin (uninformed search) nhưng có xét đến chi phí của đường đi. UCS mở rộng các trạng thái theo tổng chi phí đường đi thấp nhất từ trạng thái ban đầu đến trạng thái hiện tại. UCS sử dụng một hàng đợi ưu tiên (priority queue), đảm bảo tìm được lời giải tối ưu về tổng chi phí, không chỉ về số bước.

    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State): Ma trận 3x3 chứa 8 ô số (1–8) và một ô trống (0), có thể sắp xếp ngẫu nhiên nhưng phải khả giải.

    Tập hành động (Actions): Ô trống có thể di chuyển lên, xuống, trái, phải – tùy thuộc vào vị trí của nó trong lưới.

    Hàm chuyển trạng thái (Transition Model): Tạo trạng thái mới bằng cách hoán đổi ô trống với ô liền kề theo hướng di chuyển.

    Kiểm tra mục tiêu (Goal Test): Kiểm tra xem trạng thái hiện tại có khớp với trạng thái đích hay không.

    Hàm chi phí (Path Cost): Mỗi hành động có thể gán chi phí là 1 (nếu đồng đều) hoặc một giá trị khác nếu mô hình mở rộng. UCS ưu tiên mở rộng trạng thái có tổng chi phí nhỏ nhất.

    Hoạt động của thuật toán UCS
    Sử dụng một hàng đợi ưu tiên (priority queue) với ưu tiên là tổng chi phí đường đi (g(n)).

    Khởi tạo: Đưa trạng thái ban đầu vào hàng đợi với chi phí 0.

    Lặp lại:

    Lấy trạng thái có chi phí nhỏ nhất khỏi hàng đợi.

    Nếu đó là trạng thái đích → trả về chuỗi hành động tương ứng.

    Nếu không, tạo các trạng thái con hợp lệ.

    Thêm hoặc cập nhật các trạng thái con vào hàng đợi nếu:

    Chúng chưa được duyệt.

    Hoặc tìm thấy đường đi tốt hơn đến chúng (chi phí thấp hơn).

    Quá trình dừng khi tìm được trạng thái đích hoặc hàng đợi rỗng.

    UCS tương đương với Dijkstra’s algorithm nếu áp dụng cho tìm đường đi ngắn nhất trên đồ thị.

    Solution:
    Trả về chuỗi hành động biến trạng thái ban đầu thành trạng thái đích, với tổng chi phí thấp nhất (dù số bước có thể không ít nhất nếu chi phí mỗi bước khác nhau).

    Trong bài toán 8-Puzzle với chi phí mỗi bước = 1, UCS sẽ giống với BFS trong kết quả (vì tổng chi phí = số bước).

    Hiệu suất
    Ưu điểm:
    Luôn tìm được lời giải tối ưu (chi phí thấp nhất).

    Ứng dụng rộng rãi trong các bài toán có chi phí hành động không đồng đều.

    Tổng quát hơn BFS.

    Nhược điểm:
    Chi phí tính toán và bộ nhớ cao nếu không có giới hạn độ sâu.

    Nếu tất cả chi phí đều bằng nhau thì hiệu suất kém hơn BFS vì tốn công duy trì hàng đợi ưu tiên.
    
Iterative Deepening Depth-First Search (IDDFS)
![IDDFS](https://github.com/user-attachments/assets/49b7d614-dde0-42a2-9f81-44f28c92956a)

Iterative Deepening Depth-First Search (IDDFS) là một kỹ thuật kết hợp giữa DFS (Depth-First Search) và BFS (Breadth-First Search) nhằm khai thác ưu điểm của cả hai: bộ nhớ tiết kiệm như DFS nhưng vẫn đảm bảo tìm được lời giải tối ưu như BFS. IDDFS đặc biệt phù hợp với các bài toán tìm kiếm có không gian trạng thái rộng nhưng độ sâu lời giải không quá lớn, ví dụ như bài toán 8-Puzzle.

    Các thành phần của bài toán tìm kiếm trong 8-Puzzle
    Trạng thái ban đầu (Initial State)
    Cấu hình lưới 3x3 với 8 ô số (1–8) và 1 ô trống (0), xuất phát từ một trạng thái bất kỳ nhưng hợp lệ (có thể giải được).

    Tập hành động (Actions)
    Tại mỗi trạng thái, ô trống có thể được di chuyển lên, xuống, trái hoặc phải, tùy vào vị trí hiện tại.

    Hàm chuyển trạng thái (Transition Model)
    Thực hiện một hành động → tạo trạng thái mới bằng cách đổi chỗ ô trống với ô liền kề tương ứng.

    Kiểm tra mục tiêu (Goal Test)
    Kiểm tra xem trạng thái hiện tại có giống với trạng thái đích (thường là trạng thái đã sắp xếp đúng theo thứ tự từ 1 đến 8, với 0 ở cuối) hay không.

    Hàm chi phí (Path Cost)
    Mỗi hành động có chi phí bằng 1 → tổng chi phí là số bước di chuyển.

    Hoạt động của thuật toán IDDFS
    Thuật toán IDDFS thực hiện như sau:

    Gọi một hàm tìm kiếm theo chiều sâu (DFS) với giới hạn độ sâu d.

    Bắt đầu với d = 0, sau đó tăng dần (d = 1, 2, 3,...) cho đến khi tìm được lời giải hoặc đạt giới hạn cụ thể.

    Ở mỗi vòng lặp, thuật toán sẽ tìm kiếm lại từ đầu đến độ sâu d hiện tại.

    Trong quá trình này, thuật toán không lưu toàn bộ cây trạng thái, giúp tiết kiệm đáng kể bộ nhớ.

    Solution
    Lời giải là chuỗi các hành động hợp lệ từ trạng thái đầu đến trạng thái đích. IDDFS đảm bảo lời giải ngắn nhất về số bước (giống BFS), vì nó kiểm tra các độ sâu nhỏ trước.
    
    Ưu điểm và nhược điểm của IDDFS trong 8-Puzzle
    Ưu điểm
    Đảm bảo tìm được lời giải ngắn nhất (nếu chi phí bằng nhau).

    Bộ nhớ tiêu tốn rất ít → phù hợp với không gian trạng thái lớn.

    Kết hợp được điểm mạnh của BFS và DFS.

    Hiệu quả hơn DFS thuần vì tránh vòng lặp vô tận và thiếu tối ưu.

    Nhược điểm
    Phải lặp lại việc duyệt ở các độ sâu nhỏ → chi phí thời gian tăng.

    Không sử dụng thông tin heuristic → tốc độ chậm hơn các thuật toán có thông tin (A*, IDA*).
    
