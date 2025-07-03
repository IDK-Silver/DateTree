import 'package:flutter/material.dart';

class TodoItemCard extends StatelessWidget {
  final String id;
  final String content;
  final bool isCompleted;
  final int? voteCount;
  final VoidCallback? onTap;
  final VoidCallback? onComplete;
  final VoidCallback? onDelete;

  const TodoItemCard({
    super.key,
    required this.id,
    required this.content,
    this.isCompleted = false,
    this.voteCount,
    this.onTap,
    this.onComplete,
    this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Dismissible(
      key: Key(id),
      background: Container(
        color: Theme.of(context).colorScheme.primary,
        alignment: Alignment.centerLeft,
        padding: const EdgeInsets.only(left: 20),
        child: const Icon(
          Icons.check,
          color: Colors.white,
        ),
      ),
      secondaryBackground: Container(
        color: Theme.of(context).colorScheme.error,
        alignment: Alignment.centerRight,
        padding: const EdgeInsets.only(right: 20),
        child: const Icon(
          Icons.delete,
          color: Colors.white,
        ),
      ),
      confirmDismiss: (direction) async {
        if (direction == DismissDirection.startToEnd) {
          onComplete?.call();
          return false;
        } else if (direction == DismissDirection.endToStart) {
          return await _showDeleteConfirmation(context);
        }
        return false;
      },
      onDismissed: (direction) {
        if (direction == DismissDirection.endToStart) {
          onDelete?.call();
        }
      },
      child: Card(
        margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        child: ListTile(
          onTap: onTap,
          leading: IconButton(
            icon: Icon(
              isCompleted
                  ? Icons.check_circle
                  : Icons.radio_button_unchecked,
              color: isCompleted
                  ? Theme.of(context).colorScheme.primary
                  : null,
            ),
            onPressed: onComplete,
          ),
          title: Text(
            content,
            style: TextStyle(
              decoration: isCompleted
                  ? TextDecoration.lineThrough
                  : TextDecoration.none,
              color: isCompleted ? Colors.grey : null,
            ),
          ),
          subtitle: voteCount != null && voteCount! > 0
              ? Text(
                  '${voteCount!} votes',
                  style: TextStyle(
                    color: Theme.of(context).colorScheme.primary,
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                  ),
                )
              : null,
          trailing: voteCount != null && voteCount! > 0
              ? Icon(
                  Icons.how_to_vote,
                  size: 16,
                  color: Theme.of(context).colorScheme.primary,
                )
              : null,
        ),
      ),
    );
  }

  Future<bool> _showDeleteConfirmation(BuildContext context) async {
    return await showDialog<bool>(
          context: context,
          builder: (BuildContext context) {
            return AlertDialog(
              title: const Text('Delete Todo'),
              content: const Text('Are you sure you want to delete this todo?'),
              actions: [
                TextButton(
                  onPressed: () => Navigator.of(context).pop(false),
                  child: const Text('Cancel'),
                ),
                TextButton(
                  onPressed: () => Navigator.of(context).pop(true),
                  style: TextButton.styleFrom(
                    foregroundColor: Theme.of(context).colorScheme.error,
                  ),
                  child: const Text('Delete'),
                ),
              ],
            );
          },
        ) ??
        false;
  }

}