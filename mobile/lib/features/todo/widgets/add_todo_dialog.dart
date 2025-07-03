import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/providers/todo_provider.dart';
import '../../../shared/widgets/atoms/primary_button.dart';
import '../../../shared/widgets/atoms/custom_text_field.dart';

class AddTodoDialog extends ConsumerStatefulWidget {
  final int calendarId;
  final VoidCallback? onTodoAdded;

  const AddTodoDialog({
    super.key,
    required this.calendarId,
    this.onTodoAdded,
  });

  @override
  ConsumerState<AddTodoDialog> createState() => _AddTodoDialogState();
}

class _AddTodoDialogState extends ConsumerState<AddTodoDialog> {
  final _formKey = GlobalKey<FormState>();
  final _contentController = TextEditingController();
  bool _isLoading = false;

  @override
  void dispose() {
    _contentController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Add Todo'),
      content: Form(
        key: _formKey,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              CustomTextField(
                controller: _contentController,
                labelText: 'Content',
                hintText: 'Enter todo content...',
                maxLines: 3,
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'Please enter content';
                  }
                  return null;
                },
              ),
            ],
          ),
        ),
      ),
      actions: [
        TextButton(
          onPressed: _isLoading ? null : () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        PrimaryButton(
          text: 'Add Todo',
          isLoading: _isLoading,
          width: 120,
          onPressed: _handleAddTodo,
        ),
      ],
    );
  }


  Future<void> _handleAddTodo() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      await ref.read(todoProvider(widget.calendarId).notifier).createTodo(
            content: _contentController.text.trim(),
          );

      if (mounted) {
        Navigator.of(context).pop();
        widget.onTodoAdded?.call();
        
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Todo added successfully'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Failed to add todo: $e'),
            backgroundColor: Theme.of(context).colorScheme.error,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }
}